import Foundation
import Security

struct Keychain {
    private static let service = "ai.orange.desktop"

    @discardableResult
    static func save(_ value: String, for key: String) -> Bool {
        let data = Data(value.utf8)
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
        ]
        let attributes: [String: Any] = [
            kSecValueData as String: data,
            kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly,
        ]

        let updateStatus = SecItemUpdate(query as CFDictionary, attributes as CFDictionary)
        if updateStatus == errSecItemNotFound {
            var createQuery = query
            createQuery[kSecValueData as String] = data
            createQuery[kSecAttrAccessible as String] = kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly
            let createStatus = SecItemAdd(createQuery as CFDictionary, nil)
            if createStatus != errSecSuccess {
                Logger.error("Keychain add failed (OSStatus=\(createStatus)) for account '\(key)'")
                return false
            }
            return true
        }

        if updateStatus != errSecSuccess {
            Logger.error("Keychain update failed (OSStatus=\(updateStatus)) for account '\(key)'")
            return false
        }
        return true
    }

    static func load(_ key: String) -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne,
        ]

        var item: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &item)
        guard status == errSecSuccess else {
            if status != errSecItemNotFound {
                Logger.error("Keychain load failed (OSStatus=\(status)) for account '\(key)' service='\(service)'")
            }
            return nil
        }
        guard let data = item as? Data, let value = String(data: data, encoding: .utf8), !value.isEmpty else {
            Logger.error("Keychain load returned empty or non-UTF8 data for account '\(key)'")
            return nil
        }
        return value
    }

    static func delete(_ key: String) {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
        ]
        let status = SecItemDelete(query as CFDictionary)
        if status != errSecSuccess && status != errSecItemNotFound {
            Logger.error("Keychain delete failed (\(status)) for key \(key)")
        }
    }
}
