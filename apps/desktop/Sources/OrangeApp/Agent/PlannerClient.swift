import Foundation

struct PlanRequest: Codable {
    let schemaVersion: Int
    let sessionId: String
    let transcript: String
    let screenshotBase64: String?
    let axTreeSummary: String?
    let app: AppMetadata
    let preferences: PlannerPreferences?

    enum CodingKeys: String, CodingKey {
        case schemaVersion = "schema_version"
        case sessionId = "session_id"
        case transcript
        case screenshotBase64 = "screenshot_base64"
        case axTreeSummary = "ax_tree_summary"
        case app
        case preferences
    }
}

struct PlanSimulationRequest: Codable {
    let schemaVersion: Int
    let sessionId: String
    let transcript: String
    let app: AppMetadata
    let preferences: PlannerPreferences?

    enum CodingKeys: String, CodingKey {
        case schemaVersion = "schema_version"
        case sessionId = "session_id"
        case transcript
        case app
        case preferences
    }
}

struct PlannerPreferences: Codable {
    let preferredModel: String?
    let locale: String?
    let lowLatency: Bool

    enum CodingKeys: String, CodingKey {
        case preferredModel = "preferred_model"
        case locale
        case lowLatency = "low_latency"
    }
}

struct PlannerStreamEvent: Codable, Identifiable {
    let sessionId: String
    let event: String
    let message: String
    let progress: Int?
    let stepId: String?
    let severity: String?
    let timestamp: String?

    var id: String {
        "\(sessionId)-\(stepId ?? "none")-\(event)-\(message)-\(progress ?? -1)"
    }

    enum CodingKeys: String, CodingKey {
        case sessionId = "session_id"
        case event
        case message
        case progress
        case stepId = "step_id"
        case severity
        case timestamp
    }
}

struct VerifyResponse: Codable {
    let schemaVersion: Int
    let sessionId: String
    let status: String
    let confidence: Double
    let reason: String?

    enum CodingKeys: String, CodingKey {
        case schemaVersion = "schema_version"
        case sessionId = "session_id"
        case status
        case confidence
        case reason
    }
}

struct PlanSimulationResponse: Codable {
    let schemaVersion: Int
    let sessionId: String
    let isValid: Bool
    let parseErrors: [String]
    let riskLevel: String
    let requiresConfirmation: Bool
    let summary: String
    let proposedActionsCount: Int
    let recoveryGuidance: String?

    enum CodingKeys: String, CodingKey {
        case schemaVersion = "schema_version"
        case sessionId = "session_id"
        case isValid = "is_valid"
        case parseErrors = "parse_errors"
        case riskLevel = "risk_level"
        case requiresConfirmation = "requires_confirmation"
        case summary
        case proposedActionsCount = "proposed_actions_count"
        case recoveryGuidance = "recovery_guidance"
    }
}

struct PlannerModelRoute: Codable {
    let app: String?
    let model: String
    let reason: String
}

struct ModelsResponse: Codable {
    let schemaVersion: Int
    let routing: [PlannerModelRoute]
    let featureFlags: [String: String]

    enum CodingKeys: String, CodingKey {
        case schemaVersion = "schema_version"
        case routing
        case featureFlags = "feature_flags"
    }
}

protocol PlannerClient {
    func plan(request: PlanRequest) async throws -> ActionPlan
    func simulate(request: PlanSimulationRequest) async throws -> PlanSimulationResponse
    func models() async throws -> ModelsResponse
    func telemetry(event: SessionTelemetryEvent) async
    func verify(
        sessionId: String,
        plan: ActionPlan,
        executionStatus: ExecutionStatus,
        reason: String?,
        beforeContext: String?,
        afterContext: String?
    ) async throws -> VerifyResponse
    func streamEvents(sessionId: String) -> AsyncThrowingStream<PlannerStreamEvent, Error>
}
