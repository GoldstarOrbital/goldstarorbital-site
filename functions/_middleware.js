// Pages _redirects accepts paths, not hostname conditions.
// Preserve the full path and query while consolidating public duplicate hosts.
export async function onRequest(context) {
  const url = new URL(context.request.url);
  if (url.hostname === 'www.goldstarorbital.com' || url.hostname === 'goldstarorbital-site.pages.dev') {
    url.hostname = 'goldstarorbital.com';
    url.protocol = 'https:';
    return Response.redirect(url.toString(), 301);
  }
  return context.next();
}
