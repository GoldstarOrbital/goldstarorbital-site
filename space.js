'use strict';
document.querySelectorAll('.hero, .arch-hero').forEach(hero => {
  const scene = document.createElement('div');
  scene.className = 'space-scene';
  scene.setAttribute('aria-hidden','true');
  scene.innerHTML = '<div class="starfield"></div><div class="space-orbit"><img class="orbiter" src="assets/orbit-satellite.svg" alt=""></div><div class="space-orbit second"><img class="orbiter" src="assets/orbit-satellite.svg" alt=""></div><i class="shooting-star"></i><i class="shooting-star s2"></i><i class="shooting-star s3"></i>';
  hero.append(scene);
  const button = document.createElement('button');
  button.className = 'motion-toggle';
  button.type = 'button';
  button.textContent = 'Pause motion';
  button.setAttribute('aria-pressed','false');
  button.addEventListener('click',()=>{
    const paused = hero.classList.toggle('motion-paused');
    button.textContent = paused ? 'Resume motion' : 'Pause motion';
    button.setAttribute('aria-pressed',String(paused));
  });
  hero.append(button);
});
