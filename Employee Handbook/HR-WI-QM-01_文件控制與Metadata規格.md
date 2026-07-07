---
doc_id: HR-WI-QM-01
title: 文件控制與Metadata規格
doc_type: work_instruction
version: v0.3
status: draft
effective_date:
owner_department: 人事課
author: 蔡家瑋
reviewer:
approver:
last_updated: 2026-07-07
related_documents:
  - HR-PR-QM-01
  - HR-FM-QM-01
  - HR-FM-QM-02
  - HR-FM-QM-03
  - HR-FM-QM-04
---

# 文件控制與Metadata規格 (HR-WI-QM-01)

## 文件資訊

| 欄位 | 內容 |
| --- | --- |
| 文件編號 | HR-WI-QM-01 |
| 文件名稱 | 文件控制與Metadata規格 |
| 文件類型 | 作業指導書 |
| 版本 | v0.3 |
| 狀態 | 草稿（未發行） |
| 制定單位 | 人事課 |
| 制定者 | 蔡家瑋 |
| 審核者 |  |
| 核准者 |  |
| 生效日 |  |
| 最後更新日 | 2026-07-07 |

## 文件履歷

| 版本 | 日期 | 修訂內容 | 制定者 | 審核者 | 核准者 |
| --- | --- | --- | --- | --- | --- |
| v0.1 |  | 初版草案建立 | 蔡家瑋 |  |  |
| v0.2 | 2026-07-07 | 補充命名、文件類型、版次、發布與AI檢核規格 | 蔡家瑋 |  |  |
| v0.3 | 2026-07-07 | 補充知識庫與RAG使用之 metadata 欄位、權限分級及摘要維護規則 | 蔡家瑋 |  |  |

## 一、目的

為使 HR 文件可由人員審閱，並可由 AI、自動化腳本、Google Drive、Google Sites、PDF 產生流程及文件清單穩定讀取，特訂定本文件控制與 metadata 規格。

## 二、適用範圍

本規格適用於 `Employee Handbook` 資料夾內所有 Markdown 文件，包含手冊、程序書、作業指導書及表單。由既有 Word/PDF SOP 轉入之文件，也應依本規格補齊 metadata、文件資訊、文件履歷與狀態標示。

## 三、檔案命名規格

檔名格式固定為：

```text
{文件編號}_{文件名稱}.md
```

範例：

```text
HR-PR-ATT-04_加班申請作業程序.md
HR-FM-QM-03_文件清單與版次管制表.md
```

命名原則如下：

| 項目 | 規格 |
| --- | --- |
| 文件編號 | 應與 YAML `doc_id`、H1 標題及文件資訊表一致。 |
| 文件名稱 | 使用正式中文名稱，不使用暫名、括號備註或版本號。 |
| 分隔符號 | 文件編號與文件名稱間使用半形底線 `_`。 |
| 副檔名 | Markdown 原始檔一律使用 `.md`。PDF 匯出檔應同名使用 `.pdf`。 |
| 舊制文件 | 既有 `HR-SP-###`、`FA-SP-###` 可保留原編號，避免與已發行 SOP 失去追溯關係。 |

## 四、文件編號規格

| 編號格式 | 文件類型 | 用途 |
| --- | --- | --- |
| `HR-MN-QM-##` | 手冊 | 員工手冊、管理手冊等整體性規範。 |
| `HR-PR-{DOMAIN}-##` | 程序書 | 跨角色、跨表單或需要審核流程的作業。 |
| `HR-WI-{DOMAIN}-##` | 作業指導書 | 單一系統、單一步驟或操作型指引。 |
| `HR-FM-{DOMAIN}-##` | 表單 | 申請單、紀錄表、檢核表、公告範本。 |
| `HR-SP-###` | 舊制 HR 規範 | 既有 SOP 或尚未轉入新版編碼之文件。 |
| `FA-SP-###` | 舊制財會規範 | 與 HR 相關但權責屬財會之既有 SOP。 |

常用領域代碼如下：

| 代碼 | 領域 |
| --- | --- |
| `ATT` | 出勤、請假、加班、天災出勤 |
| `REC` | 招募、任用、勞動契約、人事資料 |
| `PER` | 績效、考核、獎懲 |
| `PAY` | 薪資、津貼、加給、獎金 |
| `SEP` | 離職、資遣、退休、移交 |
| `TRA` | 教育訓練 |
| `TRV` | 差旅 |
| `GEN` | 通用 HR、申訴、個資、性平、職安衛 |
| `QM` | 文件管理、品質管理、版次控制 |

## 五、Metadata 欄位規格

每份文件應於檔案最上方放置 YAML frontmatter：

### 5.1 基本欄位

| 欄位 | 必填 | 說明 |
| --- | --- | --- |
| `doc_id` | 是 | 文件編號，須與檔名及 H1 標題一致。 |
| `title` | 是 | 文件名稱，須與檔名及 H1 標題一致。 |
| `doc_type` | 是 | `manual`、`procedure`、`work_instruction`、`form`。 |
| `version` | 是 | 版次，未發行草稿自 `v0.1` 起版。 |
| `status` | 是 | `draft`、`review`、`approved`、`active`、`archived`。 |
| `effective_date` | 條件必填 | 僅正式生效文件填寫；草稿及規劃中文件留空。 |
| `owner_department` | 是 | 文件權責單位，HR 文件預設為人事課。 |
| `author` | 是 | 制定者。 |
| `reviewer` | 條件必填 | 送審後填寫；草稿可留空。 |
| `approver` | 條件必填 | 核准後填寫；草稿可留空。 |
| `last_updated` | 是 | 最後更新日，供 AI 掃描與文件清單更新。 |
| `source_document` | 條件必填 | 由既有 Word/PDF 轉入時填寫來源檔名。 |
| `related_documents` | 是 | 相關文件編號清單。無相關文件時使用 `[]`。 |

### 5.2 知識庫與 RAG 欄位

為支援未來文件入口、全文搜尋、權限控管及 AI 問答，文件 metadata 應預留下列欄位。草稿文件可先填入暫定值，正式發行前應完成確認。

| 欄位 | 必填 | 說明 |
| --- | --- | --- |
| `summary` | 條件必填 | 文件短摘要，建議 30 至 80 字。`active` 文件正式發行前必填；`draft` 文件可填「草稿，待內容確認後補正式摘要」。 |
| `keywords` | 是 | 文件關鍵字清單，用於搜尋、分類及 FAQ 對應。無關鍵字時使用 `[]`。 |
| `audience` | 是 | 文件主要閱讀對象，例如 `employee`、`manager`、`hr`、`finance`、`executive`。 |
| `access_level` | 是 | 文件可見範圍，建議值：`public`、`internal`、`restricted`、`confidential`。 |
| `allowed_roles` | 是 | 可查閱或可由 AI 回答引用之角色清單。 |
| `sensitivity` | 是 | 敏感程度，建議值：`normal`、`draft`、`personal_data`、`payroll`、`disciplinary`、`confidential`。 |

### 5.3 欄位填寫原則

| 文件狀態 | `summary` | `access_level` | `allowed_roles` | `sensitivity` |
| --- | --- | --- | --- | --- |
| `active` | 必填正式摘要。 | 依文件內容判定，員工可查制度多為 `internal`。 | 依實際可見角色填寫。 | 依內容敏感度填寫。 |
| `draft` | 可填暫定摘要或「草稿，待內容確認後補正式摘要」。 | 原則上使用 `restricted`。 | 原則上限 `hr`、`executive`，必要時加入 `manager`。 | 原則上使用 `draft`，涉及薪資、個資或獎懲時提高分級。 |
| `review` | 應填接近正式之摘要。 | 原則上使用 `restricted`。 | 限審核相關角色。 | 依內容敏感度填寫。 |
| `approved` | 必填正式摘要。 | 依預定發行範圍填寫。 | 依預定發行對象填寫。 | 依內容敏感度填寫。 |
| `archived` | 保留原摘要。 | 原則上使用 `restricted`。 | 限 `hr`、`executive` 或文件管理角色。 | 保留或提高分級。 |

### 5.4 建議角色代碼

| 角色代碼 | 說明 |
| --- | --- |
| `employee` | 一般員工。 |
| `manager` | 主管或具人員管理責任者。 |
| `hr` | 人事課或 HR 文件管理者。 |
| `finance` | 財會相關人員。 |
| `executive` | 經營主管或核決主管。 |
| `document_admin` | 文件管理、系統管理或知識庫維護人員。 |

### 5.5 建議權限與敏感度分級

| 欄位 | 值 | 用途 |
| --- | --- | --- |
| `access_level` | `public` | 可公開對外揭露之文件。HR 內規通常不使用此值。 |
| `access_level` | `internal` | 公司內部員工可查閱之正式制度、流程、表單。 |
| `access_level` | `restricted` | 僅特定角色可查閱，例如草稿、審核中、管理用文件。 |
| `access_level` | `confidential` | 高敏感文件，例如薪資策略、獎懲調查、人事個案資料。 |
| `sensitivity` | `normal` | 一般制度或表單。 |
| `sensitivity` | `draft` | 尚未正式發行之草稿或規劃文件。 |
| `sensitivity` | `personal_data` | 涉及個人資料、人事資料或申訴紀錄。 |
| `sensitivity` | `payroll` | 涉及薪資、獎金、津貼、扣款或財務給付。 |
| `sensitivity` | `disciplinary` | 涉及獎懲、調查、違規或考核處理。 |
| `sensitivity` | `confidential` | 公司指定機密或高度限制資料。 |

### 5.6 Metadata 範例

正式發行且員工可查之文件：

```yaml
---
doc_id: HR-PR-ATT-01
title: 員工請假管理程序
doc_type: procedure
version: v1.0
status: active
effective_date: 2026-08-01
owner_department: 人事課
author: 蔡家瑋
reviewer: 待填
approver: 待填
last_updated: 2026-07-07
summary: 規範員工請假申請、緊急請假補辦、代理交接及考勤影響。
keywords:
  - 請假
  - 特休
  - 病假
  - 考勤
audience:
  - employee
  - manager
  - hr
access_level: internal
allowed_roles:
  - employee
  - manager
  - hr
sensitivity: normal
related_documents:
  - HR-FM-ATT-01
---
```

草稿或尚未確認之文件：

```yaml
---
doc_id: HR-PR-GEN-04
title: 職業安全衛生管理程序
doc_type: procedure
version: v0.1
status: draft
effective_date:
owner_department: 人事課
author: 蔡家瑋
reviewer:
approver:
last_updated: 2026-07-07
summary: 草稿，待內容確認後補正式摘要。
keywords: []
audience:
  - hr
access_level: restricted
allowed_roles:
  - hr
  - executive
sensitivity: draft
related_documents: []
---
```

### 5.7 摘要維護規則

`summary` 應為人工確認之短摘要，用於文件清單、搜尋結果、員工入口及 AI 回答前的文件辨識。長摘要、分段摘要、全文內容、chunk、embedding、token 統計及 AI 自動摘要，不應手動寫回每份 Markdown，應由索引程序產生並存放於 `document_index.json` 或 `document_index.db`。

| 摘要類型 | 存放位置 | 維護方式 |
| --- | --- | --- |
| 短摘要 | Markdown metadata 的 `summary` | 人工確認，正式發行前必填。 |
| 文件長摘要 | `document_index.json` / `document_index.db` | AI 或腳本產生，可刪除重建。 |
| 分段摘要 | `document_index.json` / `document_index.db` | AI 或腳本依段落產生。 |
| Embedding / 向量 | 向量資料庫或索引 DB | 自動產生，不手動維護。 |

## 六、文件狀態與版次規則

| 狀態 | 說明 | 生效日 |
| --- | --- | --- |
| `draft` | 草稿、規劃中或尚未送審文件。 | 留空 |
| `review` | 已送審，待審核者確認。 | 留空 |
| `approved` | 已核准但尚未公告或未到生效日。 | 可填預定生效日 |
| `active` | 已公告且生效，可作為正式依據。 | 必填 |
| `archived` | 已停用或被新版取代。 | 保留原生效日 |

版次原則如下：

| 版次 | 用途 |
| --- | --- |
| `v0.1`、`v0.2` | 未發行草稿或規劃版。 |
| `v1.0` | 第一次正式發行。 |
| `v1.1` | 不影響制度本質的小修，例如文字、表單欄位、流程補述。 |
| `v2.0` | 影響權利義務、流程責任、核准層級或制度架構的重大修訂。 |

## 七、文件內必要區塊

| 文件類型 | 必要區塊 |
| --- | --- |
| `manual` | 文件資訊、文件履歷、目的、適用範圍、章節條文、相關文件、附錄。 |
| `procedure` | 文件資訊、文件履歷、目的、適用範圍、權責、作業流程、作業內容、紀錄保存、相關文件。 |
| `work_instruction` | 文件資訊、文件履歷、目的、適用範圍、使用時機或前置條件、操作步驟、異常處理、相關文件。 |
| `form` | 文件資訊、文件履歷、填寫說明、表單欄位、簽核或確認欄位、紀錄保存、相關文件。 |

## 八、AI 自動化檢核規格

AI 或自動化腳本應至少檢查：

1. 檔名、`doc_id`、H1 標題是否一致。
2. YAML frontmatter 是否具備必要欄位。
3. `status: active` 文件是否具備 `effective_date`、審核者與核准者。
4. `draft` 或 `review` 文件是否被錯誤放入正式公告清單。
5. `related_documents` 是否能對應到實際存在的文件。
6. 程序書是否具備目的、適用範圍、權責、作業流程、作業內容、紀錄保存與相關文件。
7. 表單是否具備填寫說明、欄位、簽核或確認欄位、紀錄保存。
8. 匯出 PDF 時，流程圖、表格及簽核欄是否避免跨頁截斷。
9. `summary`、`keywords`、`audience`、`access_level`、`allowed_roles`、`sensitivity` 是否符合文件狀態及權限規則。
10. AI 查詢索引是否只納入使用者角色可查閱之文件；不得先檢索無權限文件後再交由模型自行判斷能否回答。

## 九、RAG 與知識庫索引原則

未來建置 AI 查詢或 chatbot 時，Markdown 文件仍為單一真相來源，索引檔僅作為可重建之查詢快取。

索引程序應遵循下列原則：

1. 預設僅索引 `status: active` 且使用者角色具備查閱權限之文件。
2. `draft`、`review` 文件不得提供一般員工查詢；如主管或 HR 查詢草稿，回答中應明確標示「草稿，尚未正式發行」。
3. 檢索前應先依 `allowed_roles`、`access_level`、`sensitivity` 過濾文件，不得將未授權內容送入 AI model context。
4. AI 回答應附來源文件編號、文件名稱、版本及段落或章節。
5. 查無正式依據時，AI 應回答「查無正式文件依據」，不得自行推測制度。
6. `document_index.json`、`document_index.db`、向量索引及快取均應可由 Markdown 重新產生，不作為正式制度內容來源。

## 十、發布輸出建議

Markdown 應作為單一來源檔。對員工發布時，建議同步產出：

| 輸出 | 用途 |
| --- | --- |
| Markdown | 原始維護、AI 比對、Git 版本控管。 |
| PDF | 正式公告、簽核留存、Google Sites 嵌入。 |
| HTML | 內部網站瀏覽與搜尋。 |
| 文件清單 | 管控目前有效版、草稿版與已封存文件。 |

Google Drive 可存放 Markdown 原始檔與 PDF 發行檔；Google Sites 建議嵌入 PDF 或發布後 HTML，不建議直接嵌入 Markdown 原始檔。
