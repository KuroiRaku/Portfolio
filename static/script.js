'use strict';
(function() {

    var backlink = document.getElementById('backlink');
    if (backlink) {
        backlink.addEventListener('click', function() {
            window.location.href = document.referrer;
        });
    }

    var deleteButtons = document.getElementsByClassName('delete-btn');
    if (deleteButtons) {
        Array.prototype.forEach.call(deleteButtons, function(button) {
            button.addEventListener('click', function(e) {
                if (!window.confirm('Are you sure?'))
                    e.preventDefault();
            });
        });
    }

    var textArea = document.getElementsByClassName('simplemde')[0];
    if (textArea)
        var simplemde = new SimpleMDE({textArea});

    document.addEventListener('keypress', function(e) {
        if (e.ctrlKey && e.key === 'q') {
            var loginBtn = document.getElementById('btn-login');
            if (loginBtn) {
                if (loginBtn.classList.contains('hidden')) {
                    loginBtn.classList.remove('hidden');
                } else {
                    loginBtn.classList.add('hidden');
                }
            }
        }
    });

})();

function toggle_display() {
  var web_dev = document.getElementById("web");
  var web_dev = document.getElementById("web_button");
  var game_dev_button = document.getElementById("game_dev");
  var web_dev_button = document.getElementById("game_button");
  if (web_dev.style.display === "none") {
    web_dev.style.display = "block";
    game_dev.style.display = "none";
    game_dev_button.style.backgroundColor ="#e7e7e7";
    web_dev_button.style.backgroundColor = "#4CAF50";
  } else {
    web_dev.style.display = "none";
    game_dev.style.display = "block";
    game_dev_button.style.backgroundColor ="#dddddd";
    web_dev_button.style.backgroundColor = "#4CAF50;";
  }
}
