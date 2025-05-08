// 토큰 확인 및 로그인 상태 업데이트
document.addEventListener("DOMContentLoaded", function () {
  const token = localStorage.getItem("token");
  const loginStatusElement = document.getElementById("login-status");

  if (token) {
    // 토큰이 있으면 로그아웃 링크로 변경
    loginStatusElement.innerHTML = '<a href="#" id="logout-link">로그아웃</a>';

    // 로그아웃 이벤트 리스너 추가
    document
      .getElementById("logout-link")
      .addEventListener("click", function (e) {
        e.preventDefault();
        localStorage.removeItem("token");
        window.location.href = "/";
      });
  }
});
