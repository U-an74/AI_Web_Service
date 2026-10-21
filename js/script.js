const issueInput = document.getElementById("issueInput");
const generateBtn = document.getElementById("generateBtn");
const message = document.getElementById("message");
const resultCard = document.getElementById("resultCard");
const reportText = document.getElementById("reportText");

generateBtn.addEventListener("click", async () => {
  const issue = issueInput.value;

  message.textContent = "생성 중입니다...";
  resultCard.classList.add("hidden");
  reportText.textContent = "";
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
        message.textContent = "문제를 입력해 주세요.";
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