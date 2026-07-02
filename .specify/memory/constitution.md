<!--
SYNC IMPACT REPORT
==================
- Version change: [CONSTITUTION_VERSION] -> 1.0.0
- List of modified principles:
  - [PRINCIPLE_1_NAME] -> I. 程式碼品質 (Code Quality)
  - [PRINCIPLE_2_NAME] -> II. 測試標準 (Testing Standards)
  - [PRINCIPLE_3_NAME] -> III. 使用者體驗一致性 (User Experience Consistency)
  - [PRINCIPLE_4_NAME] -> IV. 效能要求 (Performance Requirements)
  - [PRINCIPLE_5_NAME] -> Removed (Not required)
- Added sections:
  - ## 技術決策與實作選擇 (Technical Decisions & Implementation Choices)
  - ## 開發流程與品質關卡 (Development Workflow & Quality Gates)
- Removed sections:
  - None
- Templates requiring updates:
  - ✅ updated: `.specify/templates/plan-template.md` (Added specific gates for code quality, testing, UX, and performance)
  - ✅ updated: `.specify/templates/tasks-template.md` (Updated test guidelines to mandatory per new constitution)
  - ✅ updated: `.specify/templates/spec-template.md` (Added prompts/guidance for UX & performance criteria)
- Follow-up TODOs:
  - None
-->

# SpecKit .NET CLI Demo 憲法

## Core Principles

### I. 程式碼品質 (Code Quality)
確保所有程式碼具備高度可讀性、低耦合度與高內聚性。所有提交的程式碼皆須符合團隊定義的風格指南，並通過靜態程式碼分析。實作時應避免過度設計，注重模組的清晰度與未來可維護性。

### II. 測試標準 (Testing Standards)
測試是程式碼品質與系統穩定性的基石。所有新功能與現有功能的修改，均必須包含單元測試（Unit Tests）與整合測試（Integration Tests）。實行測試驅動開發（TDD）或確保關鍵路徑的測試覆蓋率至少達到 80%。

### III. 使用者體驗一致性 (User Experience Consistency)
不論是終端機命令列介面（CLI）還是圖形介面（GUI），都必須提供一致且符合直覺的互動體驗。所有錯誤訊息、提示資訊與操作邏輯，應遵循統一的格式、命名空間與錯誤碼規範，確保使用者體驗的平滑與一致。

### IV. 效能要求 (Performance Requirements)
系統設計與實作應注重資源利用率（如 CPU、記憶體與磁碟 I/O）與回應速度。所有主要操作與 API 呼叫需設定明確的效能基準（Baselines），避免不必要的資源浪費，並在關鍵路徑中實施效能檢測與監控。

## 技術決策與實作選擇

本專案的所有技術決策（包括但不限於第三方套件的引進、系統架構設計與開發框架選擇）均應以上述四項核心原則為指導：
1. **技術選型**：優先考慮效能表現優異、測試友善且符合程式碼品質規範的解決方案。
2. **實作選擇**：在面臨技術折衷（Trade-offs）時，應優先保證使用者體驗的一致性與系統穩定性，並透過效能測試與測試覆蓋率來量化驗證決策的正確性。

## 開發流程與品質關卡

為落實本憲法之原則，開發流程中應實施以下品質關卡：
1. **代碼審查（Code Review）**：所有合併請求（PR）必須經過審查，確認無違反核心原則，且程式碼品質符合標準。
2. **自動化驗證**：在 CI/CD 流程中自動執行所有測試與效能基線測試。未通過品質關卡（如測試失敗、覆蓋率未達標、靜態分析警告）的程式碼禁止合併至主分支。

## Governance

1. **憲法效力**：本憲法為專案開發之最高指導原則。任何技術決策或實作選擇若與本憲法衝突，必須在設計文件（plan.md）中明確說明合理化原因（Justification），並獲得專案維護者或團隊的正式批准。
2. **修訂程序**：本憲法的修訂需經由團隊討論並達成共識。修訂提案應以 Pull Request 形式提交，通過後更新版本號與修訂日期。
3. **合規評估**：團隊應定期審查專案的合規性，以評估程式碼品質、測試覆蓋率、UX 與效能是否持續符合憲法要求。

**Version**: 1.0.0 | **Ratified**: 2026-07-02 | **Last Amended**: 2026-07-02
