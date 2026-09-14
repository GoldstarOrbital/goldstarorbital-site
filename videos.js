'use strict';
document.querySelectorAll('[data-video]').forEach(link=>{
  link.addEventListener('click',event=>{
    if(event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
    event.preventDefault();
    const frame=document.createElement('iframe');
    frame.src='https://www.youtube-nocookie.com/embed/'+encodeURIComponent(link.dataset.video)+'?autoplay=1';
    frame.title=link.getAttribute('aria-label');
    frame.allow='autoplay; encrypted-media; picture-in-picture';
    frame.allowFullscreen=true;
    link.replaceWith(frame);
    frame.focus();
  });
});
