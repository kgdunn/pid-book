// Python for the book's "Run in browser" buttons. Runs in a Web Worker, so the
// page stays responsive while Pyodide loads and while an example computes.
// See my-extensions/run_in_browser.py for the design.
//
// Protocol. The page posts {id, source, filename, datasets}; the worker answers
// {id, result} with result = {stdout, error, figures: [...]}, or {status} while
// it is loading packages.

const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v0.28.3/full/";
importScripts(`${PYODIDE_URL}pyodide.js`);

// Imports that Pyodide does not ship, mapped to what micropip should install.
// process-improve goes in with deps=False: its wheel pins versions (scikit-learn)
// newer than the Pyodide distribution, and the ones Pyodide has are enough.
const MICROPIP = { plotly: ["plotly"], pyDOE3: ["pyDOE3"], openpyxl: ["openpyxl"], tqdm: ["tqdm"] };
const PROCESS_IMPROVE_DEPS = ["numpy", "pandas", "scipy", "scikit-learn", "statsmodels", "patsy", "pydantic", "pyyaml"];

const SETUP = `
import base64, contextlib, io, json, sys, traceback

NAMESPACE = {"__name__": "__main__"}   # one namespace per chapter, as in CI
FIGURES = []
DATASETS = {}

def _wanted(name, source):
    return name in sys.modules or (name in source and _importable(name))

def _patch(source=""):
    """Capture fig.show() / plt.show() and redirect openmv.net reads. Idempotent.

    A module is patched once it is imported, or before the block that will import
    it runs, so a block that imports and plots in one go is covered."""
    if _wanted("plotly", source):
        import plotly.basedatatypes as bd, plotly.io as pio
        if not getattr(bd.BaseFigure.show, "_pid", False):
            from plotly.offline import get_plotlyjs_version
            def show(fig, *args, **kwargs):
                FIGURES.append({"kind": "plotly", "json": fig.to_json(), "js": get_plotlyjs_version()})
            show._pid = True
            bd.BaseFigure.show = show
            pio.show = show
    if _wanted("matplotlib", source):
        import matplotlib
        matplotlib.use("Agg", force=True)
        import matplotlib.pyplot as plt
        if not getattr(plt.show, "_pid", False):
            def mpl_show(*args, **kwargs):
                for num in plt.get_fignums():
                    buf = io.BytesIO()
                    plt.figure(num).savefig(buf, format="png", dpi=110, bbox_inches="tight")
                    FIGURES.append({"kind": "png", "data": base64.b64encode(buf.getvalue()).decode()})
                plt.close("all")
            mpl_show._pid = True
            plt.show = mpl_show
    if _wanted("pandas", source):
        import pandas as pd
        if not getattr(pd.read_csv, "_pid", False):
            original = pd.read_csv
            def read_csv(path, *args, **kwargs):
                # Pyodide has no sockets, so pandas cannot open a URL itself: fetch it
                # through the browser. openmv.net sends CORS headers, so the file comes
                # from there; the copy the build bundles covers an outage.
                if isinstance(path, str) and path.startswith(("http://", "https://")):
                    try:
                        path = _get(path)
                    except Exception:
                        if path not in DATASETS:
                            raise
                        path = _get(DATASETS[path])
                return original(path, *args, **kwargs)
            read_csv._pid = True
            pd.read_csv = read_csv

def _get(url):
    """Fetch text synchronously (allowed in a worker). Unlike pyodide.http.open_url,
    a 404 raises instead of handing pandas the error page to parse as data."""
    from js import XMLHttpRequest
    request = XMLHttpRequest.new()
    request.open("GET", url, False)
    request.send(None)
    if not 200 <= request.status < 300:
        raise OSError(f"HTTP {request.status} fetching {url}")
    return io.StringIO(request.responseText)

def _importable(name):
    import importlib.util
    return importlib.util.find_spec(name) is not None

def run_block(source, filename, datasets):
    DATASETS.update(json.loads(datasets))
    FIGURES.clear()
    _patch(source)
    out = io.StringIO()
    error = None
    try:
        code = compile(source, filename, "exec")
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            exec(code, NAMESPACE)
    except BaseException:
        kind, exc, tb = sys.exc_info()
        frames = [f for f in traceback.extract_tb(tb) if f.filename == filename]
        error = "".join(traceback.format_list(frames)) + "".join(traceback.format_exception_only(kind, exc))
    return json.dumps({"stdout": out.getvalue(), "error": error, "figures": list(FIGURES)})
`;

async function boot() {
  self.postMessage({ status: "Loading Python..." });
  const pyodide = await loadPyodide({ indexURL: PYODIDE_URL });
  await pyodide.loadPackage("micropip");
  pyodide.runPython(SETUP);
  return pyodide;
}

const ready = boot();
const installed = new Set();

async function installFor(pyodide, source) {
  const imports = pyodide.pyimport("pyodide.code").find_imports(source).toJs();
  // pandas finds plotly through an entry point, from a string, not an import:
  // pd.options.plotting.backend = "plotly".
  if (/["']plotly["']/.test(source)) imports.push("plotly");
  const extra = [];
  for (const name of imports) {
    if (installed.has(name)) continue;
    installed.add(name);
    if (name === "process_improve") {
      await pyodide.loadPackage(PROCESS_IMPROVE_DEPS);
      extra.push(["tqdm", "pyDOE3", "openpyxl", "plotly"]);
      self.postMessage({ status: "Installing process-improve..." });
      await pyodide.pyimport("micropip").install("process-improve", { deps: false });
    } else if (MICROPIP[name]) {
      extra.push(MICROPIP[name]);
    }
  }
  if (extra.length) await pyodide.pyimport("micropip").install(extra.flat());
  // Anything else Pyodide ships (numpy, scipy, pandas, matplotlib, ...).
  await pyodide.loadPackagesFromImports(source, { messageCallback: (m) => self.postMessage({ status: m }) });
}

// Messages are handled one at a time, in order: blocks share a namespace.
let queue = Promise.resolve();
self.onmessage = ({ data }) => {
  queue = queue.then(async () => {
    let result;
    try {
      const pyodide = await ready;
      await installFor(pyodide, data.source);
      const reply = pyodide.globals.get("run_block")(data.source, data.filename, JSON.stringify(data.datasets));
      result = JSON.parse(reply);
    } catch (err) {
      result = { stdout: "", error: String(err.message || err), figures: [] };
    }
    self.postMessage({ id: data.id, result });
  });
};
