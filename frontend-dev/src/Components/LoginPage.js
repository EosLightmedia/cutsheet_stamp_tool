import React from "react"

function LoginPage() {
  const handleLogin = () => {
    window.location.href =
      "https://account.box.com/api/oauth2/authorize?state=box_csrf_token_XD37gkUQ4ERTJic8&response_type=code&client_id=ek7onbev0qocf7rtfuov0h8xo17picca&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fapi%2Fauth"
  }

  return (
    <div>
      <button onClick={handleLogin}>Login with Box</button>
    </div>
  )
}

export default LoginPage
