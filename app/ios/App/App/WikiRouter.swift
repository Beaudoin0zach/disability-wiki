import Capacitor
import Foundation

// Capacitor's default router assumes a SPA: ANY extensionless path is answered
// with the root /index.html. This site is a 540-page Astro MPA built as
// directory indexes (/crisis/ → crisis/index.html), so under the default
// router every internal link silently "navigated" to the home page — including
// the crisis pages, which are the reason this app exists.
//
// This router resolves directory-style paths to their real index.html, and
// falls back to the built 404 page (not home) when nothing exists — a wrong
// link should LOOK wrong, not quietly land on the homepage.
struct WikiRouter: Router {
    var basePath: String = ""

    func route(for path: String) -> String {
        let pathUrl = URL(fileURLWithPath: path)

        // Files with extensions (assets, .html, pagefind indexes) pass through.
        if !pathUrl.pathExtension.isEmpty {
            return basePath + path
        }

        // Directory-style page: /crisis or /crisis/ → /crisis/index.html
        let trimmed = path.hasSuffix("/") ? String(path.dropLast()) : path
        let candidate = trimmed.isEmpty ? "/index.html" : trimmed + "/index.html"
        if FileManager.default.fileExists(atPath: basePath + candidate) {
            return basePath + candidate
        }

        // Nothing there: serve the site's own 404 page if built, else home.
        if FileManager.default.fileExists(atPath: basePath + "/404.html") {
            return basePath + "/404.html"
        }
        return basePath + "/index.html"
    }
}

class WikiBridgeViewController: CAPBridgeViewController {
    override func router() -> Router {
        WikiRouter()
    }
}
