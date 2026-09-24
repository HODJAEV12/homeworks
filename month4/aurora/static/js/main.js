/* ============================================
   AURORA HOTEL — скрипты шаблона
   1) мобильное меню   2) фон шапки при скролле
   3) появление блоков 4) фильтр номеров
   5) галерея-лайтбокс 6) аккордеон
   7) валидация формы бронирования
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {

  /* --- 1. Мобильное меню (бургер) --- */
  var burger = document.querySelector('.burger');
  var nav = document.querySelector('.nav');

  if (burger && nav) {
    burger.addEventListener('click', function () {
      nav.classList.toggle('open');
      burger.classList.toggle('open');
      burger.setAttribute('aria-expanded', nav.classList.contains('open'));
    });

    // закрываем меню после клика по ссылке
    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        nav.classList.remove('open');
        burger.classList.remove('open');
      });
    });
  }

  /* --- 2. Шапка меняет фон при прокрутке --- */
  var header = document.querySelector('.header');

  function onScroll() {
    if (!header) return;
    header.classList.toggle('scrolled', window.scrollY > 60);
  }
  onScroll();
  window.addEventListener('scroll', onScroll);

  /* --- 3. Плавное появление блоков при прокрутке --- */
  var revealItems = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });

    revealItems.forEach(function (el) { observer.observe(el); });
  } else {
    // запасной вариант для старых браузеров
    revealItems.forEach(function (el) { el.classList.add('visible'); });
  }

  /* --- 4. Фильтр номеров по типу --- */
  var filterButtons = document.querySelectorAll('.filter-btn');
  var roomCards = document.querySelectorAll('.room-card[data-type]');
  var emptyMsg = document.querySelector('.rooms-empty');

  filterButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var type = btn.dataset.filter;
      var shown = 0;

      filterButtons.forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');

      roomCards.forEach(function (card) {
        var match = (type === 'all' || card.dataset.type === type);
        card.style.display = match ? '' : 'none';
        if (match) shown++;
      });

      if (emptyMsg) emptyMsg.style.display = shown ? 'none' : 'block';
    });
  });

  /* --- 5. Галерея: увеличение фото (лайтбокс) --- */
  var lightbox = document.querySelector('.lightbox');

  if (lightbox) {
    var lightboxImg = lightbox.querySelector('img');
    var closeBtn = lightbox.querySelector('.lightbox-close');

    document.querySelectorAll('[data-lightbox]').forEach(function (item) {
      item.addEventListener('click', function () {
        var img = item.querySelector('img');
        if (!img) return;
        lightboxImg.src = img.src;
        lightboxImg.alt = img.alt;
        lightbox.classList.add('open');
        document.body.style.overflow = 'hidden';
      });
    });

    function closeLightbox() {
      lightbox.classList.remove('open');
      document.body.style.overflow = '';
    }

    closeBtn.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox) closeLightbox();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeLightbox();
    });
  }

  /* --- 6. Аккордеон «Вопросы и ответы» --- */
  document.querySelectorAll('.acc-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.closest('.acc-item');
      var panel = item.querySelector('.acc-panel');
      var isOpen = item.classList.contains('open');

      // закрываем все остальные
      document.querySelectorAll('.acc-item').forEach(function (other) {
        other.classList.remove('open');
        other.querySelector('.acc-panel').style.maxHeight = null;
      });

      if (!isOpen) {
        item.classList.add('open');
        panel.style.maxHeight = panel.scrollHeight + 'px';
      }
    });
  });

  /* --- 7. Форма бронирования: проверка полей --- */
  var form = document.querySelector('#booking-form');

  if (form) {
    var today = new Date().toISOString().split('T')[0];
    var checkIn = form.querySelector('#checkin');
    var checkOut = form.querySelector('#checkout');

    // нельзя выбрать прошедшую дату
    if (checkIn) checkIn.min = today;
    if (checkOut) checkOut.min = today;

    // дата выезда всегда позже даты заезда
    if (checkIn && checkOut) {
      checkIn.addEventListener('change', function () {
        checkOut.min = checkIn.value || today;
        if (checkOut.value && checkOut.value <= checkIn.value) checkOut.value = '';
      });
    }

    function showError(field, text) {
      var box = field.closest('.field');
      box.classList.add('invalid');
      box.querySelector('.error').textContent = text;
    }

    function clearError(field) {
      var box = field.closest('.field');
      box.classList.remove('invalid');
      box.querySelector('.error').textContent = '';
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault(); // учебный шаблон — данные никуда не отправляются
      var valid = true;

      var name = form.querySelector('#name');
      var email = form.querySelector('#email');
      var phone = form.querySelector('#phone');

      [name, email, phone, checkIn, checkOut].forEach(clearError);

      if (name.value.trim().length < 2) {
        showError(name, 'Введите имя (минимум 2 символа)');
        valid = false;
      }

      if (!/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(email.value.trim())) {
        showError(email, 'Проверьте адрес почты');
        valid = false;
      }

      if (phone.value.replace(/\D/g, '').length < 10) {
        showError(phone, 'Введите телефон полностью');
        valid = false;
      }

      if (!checkIn.value) {
        showError(checkIn, 'Выберите дату заезда');
        valid = false;
      }

      if (!checkOut.value) {
        showError(checkOut, 'Выберите дату выезда');
        valid = false;
      } else if (checkIn.value && checkOut.value <= checkIn.value) {
        showError(checkOut, 'Дата выезда должна быть позже');
        valid = false;
      }

      var msg = form.querySelector('.form-msg');

      if (valid) {
        var nights = Math.round(
          (new Date(checkOut.value) - new Date(checkIn.value)) / 86400000
        );
        msg.textContent = 'Спасибо, ' + name.value.trim() + '! Заявка на ' + nights +
          ' ноч. принята. Мы ответим на ' + email.value.trim() + ' в течение 15 минут.';
        msg.classList.add('show');
        form.reset();
      } else if (msg) {
        msg.classList.remove('show');
      }
    });
  }

  /* --- 8. Год в подвале --- */
  var yearEl = document.querySelector('#year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
});
