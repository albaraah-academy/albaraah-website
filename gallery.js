// The home page: photos open full size; galleries move between photos.
// Photos open full size; a click anywhere or Esc closes them.
(function () {
  var viewer = document.getElementById('viewer'), big = viewer.querySelector('img');
  document.querySelectorAll('.card-photo, .gallery-main').forEach(function (photo) {
    photo.tabIndex = 0;
    photo.setAttribute('role', 'button');
    function open() { big.src = photo.src; big.alt = photo.alt; viewer.showModal(); }
    photo.addEventListener('click', open);
    photo.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
  });
  viewer.addEventListener('click', function () { viewer.close(); });
  // Gallery: one main photo; the thumbnails and arrows choose which.
  document.querySelectorAll('[data-gallery]').forEach(function (gallery) {
    var main = gallery.querySelector('.gallery-main'), thumbs = [].slice.call(gallery.querySelectorAll('.gallery-thumbs button')), current = 0;
    function show(i) {
      current = (i + thumbs.length) % thumbs.length;
      var img = thumbs[current].querySelector('img');
      main.src = img.src; main.alt = img.alt;
      thumbs.forEach(function (t, n) { t.classList.toggle('is-active', n === current); });
      thumbs[current].scrollIntoView({ block: 'nearest', inline: 'nearest' });
    }
    thumbs.forEach(function (t, n) { t.addEventListener('click', function () { show(n); }); });
    gallery.querySelector('.gallery-prev').addEventListener('click', function () { show(current - 1); });
    gallery.querySelector('.gallery-next').addEventListener('click', function () { show(current + 1); });
  });
})();
  
