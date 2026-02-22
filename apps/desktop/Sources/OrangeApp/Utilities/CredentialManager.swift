import Foundation

struct CredentialManager {
    private let anthropicKeyAccount = "anthropic_api_key"

    func loadAnthropicAPIKey() -> String? {
        Keychain.load(anthropicKeyAccount)
    }

    @discardableResult
    func saveAnthropicAPIKey(_ value: String) -> Bool {
        let trimmed = value.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else { return false }
        return Keychain.save(trimmed, for: anthropicKeyAccount)
    }

    func resetAnthropicAPIKey() {
        Keychain.delete(anthropicKeyAccount)
    }

    func hasAnthropicAPIKey() -> Bool {
        guard let key = loadAnthropicAPIKey() else { return false }
        return !key.isEmpty
    }
}
