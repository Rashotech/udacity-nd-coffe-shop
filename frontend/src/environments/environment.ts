export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-cbktv2dk.us', // the auth0 domain prefix
    audience: 'udacity_coffee_shop',
    clientId: 'xkcmI1m0sJgEDkUb1f9I0nuQvBoiPjlz', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
