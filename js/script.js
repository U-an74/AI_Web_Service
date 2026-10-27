const productNameInput = document.getElementById("productNameInput");
const defectInput = document.getElementById("defectInput");
const foundProcessInput = document.getElementById("foundProcessInput");

const generateBtn = document.getElementById("generateBtn");
const message = document.getElementById("message");
const resultCard = document.getElementById("resultCard");
const resultSummary = document.getElementById("resultSummary");
const reportText = document.getElementById("reportText");

const quickStartBtn = document.getElementById("quickStartBtn");
const pageSections = document.querySelectorAll(".page-section");
const navLinks = document.querySelectorAll(".nav-link");

const default8DTitles = {
  D1: "대응팀 구성",
  D2: "문제 정의",
  D3: "임시 조치",
  D4: "근본 원인 분석",
  D5: "영구 대책 선정",
  D6: "대책 실행 및 검증",
  D7: "재발 방지",
  D8: "종료 및 공유"
};

function showPage(pageId) {
  pageSections.forEach((section) => {
    section.classList.toggle("active", section.id === pageId);
  });

  navLinks.forEach((link) => {
    link.classList.toggle("active", link.dataset.page === pageId);
  });
}

function applyRoute() {
  const hash = window.location.hash || "#home";

  if (hash === "#tool") {
    showPage("toolPage");
  } else if (hash === "#guide") {
    showPage("guidePage");
  } else {
    showPage("homePage");
  }
}

window.addEventListener("hashchange", applyRoute);

if (quickStartBtn) {
  quickStartBtn.addEventListener("click", () => {
    window.location.hash = "#tool";
  });
}

applyRoute();

function clearElement(element) {
  if (element) {
    element.innerHTML = "";
  }
}

function clearResultView() {
  if (resultCard) {
    resultCard.classList.add("hidden");
  }

  if (resultSummary) {
    resultSummary.classList.add("hidden");
    clearElement(resultSummary);
  }

  if (reportText) {
    clearElement(reportText);
  }
}

function createSummaryRow(label, value) {
  const row = document.createElement("div");
  row.className = "summary-row";

  const strong = document.createElement("strong");
  strong.textContent = label;

  const span = document.createElement("span");
  span.textContent = value || "-";

  row.appendChild(strong);
  row.appendChild(span);

  return row;
}

function renderResultSummary(productName, defect, foundProcess) {
  if (!resultSummary) {
    return;
  }

  clearElement(resultSummary);

  resultSummary.appendChild(createSummaryRow("제품명", productName || "-"));
  resultSummary.appendChild(createSummaryRow("불량 현상", defect || "-"));
  resultSummary.appendChild(createSummaryRow("발견공정", foundProcess || "-"));

  resultSummary.classList.remove("hidden");
}

function parse8DSections(report) {
  if (!report || typeof report !== "string") {
    return [];
  }

  const lines = report.replace(/\r\n/g, "\n").split("\n");
  const sections = [];
  let currentSection = null;

  for (const rawLine of lines) {
    const trimmedLine = rawLine.trim();

    const match = trimmedLine.match(/^(D[1-8])\s*[\.\-:)]?\s*(.*)$/i);

    if (match) {
      if (currentSection) {
        currentSection.body = currentSection.body.trim();
        sections.push(currentSection);
      }

      const code = match[1].toUpperCase();
      const rest = (match[2] || "").trim();

      let title = default8DTitles[code] || code;
      let body = "";

      if (rest) {
        const splitMatch = rest.match(/^(.+?)\s*[:：]\s*(.+)$/);

        if (splitMatch) {
          title = splitMatch[1].trim() || title;
          body = splitMatch[2].trim();
        } else {
          const normalizedDefaultTitle = (default8DTitles[code] || "").replace(/\s+/g, "");
          const normalizedRest = rest.replace(/\s+/g, "");

          if (normalizedRest === normalizedDefaultTitle) {
            title = rest;
            body = "";
          } else {
            title = default8DTitles[code] || code;
            body = rest;
          }
        }
      }

      currentSection = {
        code,
        title,
        body
      };
    } else if (currentSection) {
      currentSection.body += (currentSection.body ? "\n" : "") + rawLine.trim();
    }
  }

  if (currentSection) {
    currentSection.body = currentSection.body.trim();
    sections.push(currentSection);
  }

  return sections;
}

function renderPlainReport(report) {
  if (!reportText) {
    return;
  }

  clearElement(reportText);

  const plainBox = document.createElement("div");
  plainBox.className = "plain-report";
  plainBox.textContent = report || "결과가 없습니다.";

  reportText.appendChild(plainBox);
}

function render8DCards(sections) {
  if (!reportText) {
    return;
  }

  clearElement(reportText);

  sections.forEach((section) => {
    const card = document.createElement("article");
    card.className = "d-card";

    if (!section.body) {
      card.classList.add("is-empty");
    }

    const header = document.createElement("div");
    header.className = "d-header";

    const badge = document.createElement("span");
    badge.className = "d-badge";
    badge.textContent = section.code;

    const title = document.createElement("h3");
    title.className = "d-title";
    title.textContent = section.title || default8DTitles[section.code] || section.code;

    const body = document.createElement("div");
    body.className = "d-body";
    body.textContent = section.body || "-";

    header.appendChild(badge);
    header.appendChild(title);

    card.appendChild(header);
    card.appendChild(body);

    reportText.appendChild(card);
  });
}

function renderReportResult(report, productName, defect, foundProcess) {
  renderResultSummary(productName, defect, foundProcess);

  const sections = parse8DSections(report);

  if (sections.length >= 2) {
    render8DCards(sections);
  } else {
    renderPlainReport(report);
  }

  if (resultCard) {
    resultCard.classList.remove("hidden");
  }
}

if (
  generateBtn &&
  productNameInput &&
  defectInput &&
  foundProcessInput &&
  message &&
  resultCard &&
  reportText
) {
  generateBtn.addEventListener("click", async () => {
    const productName = productNameInput.value.trim();
    const defect = defectInput.value.trim();
    const foundProcess = foundProcessInput.value.trim();

    clearResultView();
    message.textContent = "";

    if (!productName) {
      message.textContent = "제품명을 입력해 주세요.";
      return;
    }

    if (!defect) {
      message.textContent = "불량 현상을 입력해 주세요.";
      return;
    }

    const issueLines = [
      `제품명: ${productName}`,
      `불량 현상: ${defect}`
    ];

    if (foundProcess) {
      issueLines.push(`발견공정: ${foundProcess}`);
    }

    const issue = issueLines.join("\n");

    message.textContent = "생성 중입니다...";
    generateBtn.disabled = true;

    try {
      const response = await fetch("/api", {
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=utf-8"
        },
        body: JSON.stringify({ issue })
      });

      const data = await response.json();

      if (!response.ok) {
        if (response.status === 400) {
          message.textContent = "제품명과 불량 현상을 입력해 주세요.";
        } else {
          message.textContent = data.error || "잠시 후 다시 시도하세요.";
        }
        return;
      }

      const report = data.report_text || "결과가 없습니다.";

      renderReportResult(report, productName, defect, foundProcess);
      message.textContent = "생성이 완료되었습니다.";
    } catch (error) {
      console.error("요청 실패:", error);
      message.textContent = "잠시 후 다시 시도하세요.";
    } finally {
      generateBtn.disabled = false;
    }
  });
}