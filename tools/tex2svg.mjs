/**
 * Render a batch of TeX expressions to standalone SVG, for the proofreading page.
 *
 * The published proof copy is served under a policy that blocks every external
 * request, so MathJax cannot run in the browser there and web fonts cannot load.
 * Rendering here instead produces SVG built from glyph outlines, which needs
 * neither.
 *
 * Reads JSON on stdin:  [{"tex": "...", "display": true|false}, ...]
 * Writes JSON on stdout: ["<svg .../>", ...], in the same order. An expression
 * that fails to parse comes back as null, so the caller can leave the original
 * source in place rather than losing it.
 *
 * `mathjax-full` is resolved from MATHJAX_DIR (the directory containing
 * node_modules), falling back to this script's own directory. ES modules
 * resolve imports relative to the importing file rather than the working
 * directory, so the location has to be given explicitly.
 */

import { pathToFileURL } from 'node:url'
import { join } from 'node:path'

const base = process.env.MATHJAX_DIR || import.meta.dirname
const load = (p) => import(pathToFileURL(join(base, 'node_modules', 'mathjax-full', 'js', p)).href)

const { mathjax } = await load('mathjax.js')
const { TeX } = await load('input/tex.js')
const { SVG } = await load('output/svg.js')
const { liteAdaptor } = await load('adaptors/liteAdaptor.js')
const { RegisterHTMLHandler } = await load('handlers/html.js')
const { AllPackages } = await load('input/tex/AllPackages.js')

const adaptor = liteAdaptor()
RegisterHTMLHandler(adaptor)

const doc = mathjax.document('', {
  InputJax: new TeX({ packages: AllPackages }),
  // fontCache 'local' keeps each SVG self-contained: glyph paths are defined
  // inside the element rather than referenced from a shared document-level cache.
  OutputJax: new SVG({ fontCache: 'local' }),
})

const chunks = []
for await (const chunk of process.stdin) chunks.push(chunk)
const items = JSON.parse(Buffer.concat(chunks).toString('utf8'))

process.stdout.write(
  JSON.stringify(
    items.map(({ tex, display }) => {
      try {
        return adaptor.outerHTML(doc.convert(tex, { display: !!display }))
      } catch {
        return null
      }
    }),
  ),
)
