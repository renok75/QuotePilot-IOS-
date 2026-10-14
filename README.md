# QuotePilot — iPhone App Store cloud-build project

This project packages the **latest QuotePilot PWA** as a bundled iOS app with **Capacitor 7**. It contains the existing quote builder, customer records, business settings, default labor rate, business logo, quote-specific logo, and expiration dates. It adds a **native iOS Share sheet** for an estimate summary (not a PDF).

## Important: not yet an App Store submission

- The source has been prepared and JavaScript syntax checked, but **an iOS build has not been run** in this environment. A macOS cloud runner must compile it.
- Apple Developer membership, signing certificates/provisioning, an App Store Connect record, TestFlight testing, and App Review are still required.
- Apple's App Review 4.2 requires functionality beyond a repackaged website; approval is **not guaranteed**.
- **Existing GitHub Pages/PWA data does not automatically transfer to the native app**. Before switching, export a QuotePilot backup from the web app and import it into the native app **after verifying the restore flow on a device**. WKWebView file download and print behavior must also be tested on an actual iPhone; they may need additional native integration before release.
- Customer data is saved **locally on each device**. There is no account sync, server database, or encryption-at-rest added by this project. Deleting the app may delete records.

## Repository setup

**Recommended:** use a **separate repository** named `QuotePilot-iOS`, keeping `renok75/QuotePilot-app` intact for GitHub Pages. Upload the contents of this project folder (not the ZIP itself) to the new repository. The `www/` and `scripts/` folders must retain their names. You can use GitHub Codespaces in Safari on your iPhone to upload/unzip the archive into a repo, or connect the GitHub app to ChatGPT to explore direct file workflows. Codespaces usage may incur charges.

To unpack with Codespaces terminal after uploading the ZIP to the repo workspace:

```sh
unzip -o QuotePilot-iOS-AppStore-Project.zip
rm QuotePilot-iOS-AppStore-Project.zip
git add .
git commit -m "Prepare QuotePilot iOS cloud build"
git push
```

Do **not** upload an App Store Connect `.p8` private key, signing certificate, or password into GitHub. Add those only in Codemagic's protected integration/signing settings.

## Cloud build from iPhone (Codemagic)

1. Visit https://codemagic.io/ in Safari, create an account and authorize GitHub.
2. Add the **QuotePilot-iOS** repository as a Codemagic application. Use the **codemagic.yaml** configuration.
3. Start the **`ios-simulator-check`** workflow first. It generates the Xcode project in the cloud, installs CocoaPods, and attempts an **unsigned simulator build**. It does not produce an installable iPhone IPA.
4. Enroll in the Apple Developer Program at https://developer.apple.com/programs/enroll/ and create the QuotePilot app record in https://appstoreconnect.apple.com/ . Register the **bundle ID** `com.renok75.quotepilot` (or choose your own before first submission, updating both `capacitor.config.json` and `codemagic.yaml`).
5. Create an App Store Connect API key (Users and Access → Integrations → App Store Connect API) and add it to Codemagic **Team integrations → Developer Portal**. Set up an Apple Distribution certificate and an App Store provisioning profile for the bundle ID in Codemagic's signing settings.
6. Replace `REPLACE_WITH_CODEMAGIC_APP_STORE_CONNECT_INTEGRATION` in `codemagic.yaml` with your actual Codemagic integration name. Start the **`ios-app-store`** workflow. This should generate a signed `.ipa` after configuration and successful compilation.
7. Upload the `.ipa` to App Store Connect using Codemagic's App Store publishing integration (configure `publishing` after successful signed builds), test via TestFlight, and prepare listing details/screenshots, privacy disclosures, support URL, and privacy-policy URL.

Codemagic docs: https://docs.codemagic.io/yaml-quick-start/building-an-ionic-app/ and https://docs.codemagic.io/yaml-code-signing/signing-ios/

## Notes on functionality

- The app is bundled from `www/` and does not simply load your GitHub Pages URL.
- The iOS Share sheet shares **text summary** only. `Print / Save PDF` currently uses browser printing; **test and upgrade this to native PDF sharing** before launch if it fails in WKWebView.
- Logo file picker and JSON backup/restore must be tested in the native container. In particular, downloading a JSON backup may require a Capacitor Filesystem/Share integration on iOS.
- The project does not include a subscription or payment system. If you later sell digital features, Apple In-App Purchase rules may apply.
- Replace the starter icon if you want a higher-resolution professionally designed brand mark.

## Project files

- `www/` — bundled app (HTML, service worker, manifest, icons)
- `resources/AppIcon-1024.png` — starter iOS icon
- `capacitor.config.json` — native app ID and settings
- `package.json` — Capacitor and native Share plugin
- `scripts/prepare_ios.py` — configures the generated iOS icon and metadata
- `codemagic.yaml` — unsigned simulator check and signed App Store build workflows
