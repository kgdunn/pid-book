// Python for the book's "Run in browser" buttons. Runs in a module Web Worker
// (Pyodide 314 refuses classic workers), so the page stays responsive while
// Pyodide loads and while an example computes.
// See my-extensions/run_in_browser.py for the design.
//
// Protocol. The page posts {id, source, filename, datasets}; the worker answers
// {id, result} with result = {stdout, error, figures: [...]}, or {status} while
// it is loading packages.

// The Pyodide release comes from conf.py (run_in_browser_pyodide), through the chapter
// manifest and this script's URL: ?pyodide=314.0.7.
const VERSION = new URLSearchParams(self.location.search).get("pyodide") ?? "";
if (!/^\d+\.\d+\.\w+$/.test(VERSION)) throw new Error(`no valid Pyodide version in ${self.location}`);
const PYODIDE_URL = `https://cdn.jsdelivr.net/pyodide/v${VERSION}/full/`;

// Imports that Pyodide does not ship, mapped to what micropip should install.
// process-improve goes in with deps=False: its wheel pins versions (scikit-learn)
// newer than the Pyodide distribution, and the ones Pyodide has are enough.
const MICROPIP = {
  plotly: ["plotly"],
  pyDOE3: ["pyDOE3"],
  openpyxl: ["openpyxl"],
  tqdm: ["tqdm"],
  seaborn: ["seaborn"],
};
const PROCESS_IMPROVE_DEPS = ["numpy", "pandas", "scipy", "scikit-learn", "statsmodels", "patsy", "pydantic", "pyyaml"];

// Calls that import a package inside a function, where find_imports cannot see
// it, mapped to what Pyodide should load. statsmodels draws plot_acf with
// matplotlib, and so does pandas for obj.plot(...), df.hist(), df.boxplot() and
// pandas.plotting under its default backend. ".plot.hist(" is the Plotly
// backend's spelling and is left out, so those chapters skip the download.
const LAZY = [
  [/statsmodels\.graphics/, ["matplotlib"]],
  [/\.plot\(|(?<!\.plot)\.hist\(|\.boxplot\(|\bpandas\.plotting\b|\bpd\.plotting\./, ["matplotlib"]],
];

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
                _flush_mpl()  # a matplotlib figure drawn earlier in the block comes first
                FIGURES.append({"kind": "plotly", "json": fig.to_json(), "js": get_plotlyjs_version()})
            show._pid = True
            bd.BaseFigure.show = show
            pio.show = show
    # Whenever matplotlib is installed, not only when the block names it: a library
    # may import it inside a function (statsmodels' plot_acf).
    if _importable("matplotlib"):
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

def _flush_mpl():
    """Show matplotlib figures still open, as a notebook does: plot_acf draws one
    but never calls plt.show()."""
    plt = sys.modules.get("matplotlib.pyplot")
    if plt is not None and getattr(plt.show, "_pid", False) and plt.get_fignums():
        plt.show()

def _display(value):
    """Show the value of a block's last expression, as a notebook does: the book
    ends many examples on the answer itself, such as t.ppf(p, df=dof)."""
    first = value
    if type(value).__name__ == "ndarray" and value.dtype == object and value.size:
        first = value.flat[0]  # scatter_matrix returns an array of Axes
    if value is None or type(first).__module__.partition(".")[0] in ("matplotlib", "seaborn"):
        return  # a drawing: _flush_mpl shows the figure, and its repr is noise
    if isinstance(value, dict) and {"data", "layout"} <= value.keys() and _importable("plotly"):
        _patch("plotly")
        import plotly.graph_objects as go
        value = go.Figure(value)  # a figure spec, as process-improve's .to_plotly() returns
    if hasattr(value, "to_plotly_json"):
        value.show()  # series.plot(...) under the Plotly backend
    else:
        print(repr(value))

def run_block(source, filename, datasets):
    from pyodide.code import eval_code

    DATASETS.update(json.loads(datasets))
    FIGURES.clear()
    _patch(source)
    out = io.StringIO()
    error = None
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            # A trailing ";" hides the value, as in a notebook.
            _display(eval_code(source, NAMESPACE, return_mode="last_expr", filename=filename))
    except BaseException:
        kind, exc, tb = sys.exc_info()
        frames = [f for f in traceback.extract_tb(tb) if f.filename == filename]
        error = "".join(traceback.format_list(frames)) + "".join(traceback.format_exception_only(kind, exc))
    _flush_mpl()
    return json.dumps({"stdout": out.getvalue(), "error": error, "figures": list(FIGURES)})
`;

async function boot() {
  self.postMessage({ status: "Loading Python..." });
  const { loadPyodide } = await import(`${PYODIDE_URL}pyodide.mjs`);
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
      // callKwargs: a plain call would pass {deps: false} positionally, as keep_going.
      await pyodide.pyimport("micropip").install.callKwargs("process-improve", { deps: false });
    } else if (MICROPIP[name]) {
      extra.push(MICROPIP[name]);
    }
  }
  if (extra.length) await pyodide.pyimport("micropip").install(extra.flat());
  // Anything else Pyodide ships (numpy, scipy, pandas, matplotlib, ...).
  const messageCallback = (m) => self.postMessage({ status: m });
  await pyodide.loadPackagesFromImports(source, { messageCallback });
  for (const [pattern, packages] of LAZY) {
    if (pattern.test(source)) await pyodide.loadPackage(packages, { messageCallback });
  }
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
