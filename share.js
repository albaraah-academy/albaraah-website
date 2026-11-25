// «نسخ الرابط»: copies the news link; the button says so for a moment.
document.addEventListener('click', function (e) {
  var b = e.target.closest && e.target.closest('[data-copy]');
  if (!b) return;
  var done = function () { var t = b.textContent; b.textContent = 'تم النسخ ✓'; setTimeout(function () { b.textContent = t; }, 1800); };
  if (navigator.clipboard) navigator.clipboard.writeText(b.dataset.copy).then(done, function () { prompt('انسخ الرابط:', b.dataset.copy); });
  else prompt('انسخ الرابط:', b.dataset.copy);
});
