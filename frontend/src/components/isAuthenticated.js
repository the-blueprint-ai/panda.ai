import * as Session from "supertokens-web-js/recipe/session";

export async function isAuthenticated() {
  if (await Session.doesSessionExist()) {
    return '/' + to.name;
  } else {
    return '/auth';
  }
}
