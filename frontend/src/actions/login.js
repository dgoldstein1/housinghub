import { postAuthLogin } from "../api/login"
import store from "../reducers/index"
import { setView } from "./appState"

export function setLoginField(fieldName,newValue) {
  return {
    type: "SET_LOGIN_FIELD",
    fieldName,
    newValue
  }
}

export function setLoginSuccess(jwt) {
	return {
		type : "SET_LOGIN_SUCCESS",
		jwt
	}
}


export function setLoginFailure(error) {
	return {
		type : "SET_LOGIN_ERROR",
		error
	}
}

/**
 * fires when user attempts to login
 **/
export function loginUser() {
	// Make API call to backend /auth/login
	postAuthLogin(store.getState().login.fields).then(response => {
		if (response.jwt) {
			store.dispatch(setLoginSuccess(response.jwt))
			store.dispatch(setView("new-prop"))
		} else {
			// set error in store
			store.dispatch(setLoginFailure(response.error))
		}
	})
}