const productNameInput = document.getElementById("productNameInput");
const defectInput = document.getElementById("defectInput");
const foundProcessInput = document.getElementById("foundProcessInput");

const generateBtn = document.getElementById("generateBtn");
const message = document.getElementById("message");
const resultCard = document.getElementById("resultCard");
const reportText = document.getElementById("reportText");

const quickStartBtn = document.getElementById("quickStartBtn");
const pageSections = document.querySelectorAll(".page-section");
const navLinks = document.querySelectorAll(".nav-link");

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

if (generateBtn && productNameInput && defectInput && foundProcessInput && message && resultCard && reportText) {
  generateBtn.addEventListener("click", async () => {
    const productName = productNameInput.value.trim();
    const defect = defectInput.value.trim();
    const foundProcess = foundProcessInput.value.trim();

    resultCard.classList.add("hidden");
    reportText.textContent = "";

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

      reportText.textContent = data.report_text || "결과가 없습니다.";
      resultCard.classList.remove("hidden");
      message.textContent = "생성이 완료되었습니다.";
    } catch (error) {
      console.error("요청 실패:", error);
      message.textContent = "잠시 후 다시 시도하세요.";
    } finally {
      generateBtn.disabled = false;
    }
  });