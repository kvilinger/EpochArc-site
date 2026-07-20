export function onRequest(context) {
  const url = new URL(context.request.url);

  if (url.hostname === 'www.epoch-arc.com') {
    url.protocol = 'https:';
    url.hostname = 'epoch-arc.com';
    url.port = '';
    return Response.redirect(url.toString(), 301);
  }

  return context.next();
}
