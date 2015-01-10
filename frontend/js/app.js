
/**
 * Инициализируем приложение только тогда,
 * когда DOM готов
 */
$(function() {

    /**
     * Очень простой объект приложения
     * с ручным удовлетворением зависимостей
     *
     * @constructor
     */
    var _App = function() {
        this.modules = {};
    };
    _App.prototype = {
        /**
         * Функция регистрирует модель в приложении
         * @param name
         * @param module
         */
        register: function(name, module) {
            if (typeof module.init === 'function') {
                module.init(this, this.modules);
            }
            this.modules[name] = module;
        },

        /**
         * Получаем модуль, если такого модуля нет, то Exception с кодом 1
         * @param name
         * @throws Error
         */
        getModule: function(name) {
             if (this.modules['name']) {
                return this.modules['name'];
             } else {
                 throw new Error('This module is not registered!', 1);
             }
        },

        /**
         * Перезагружаем страницу
         */
        reload: function() {
            window.location.reload();
        }
    };
    window.App = new _App();

    /**
     * Модуль запуска сбора данных с сайта avto.ru
     */
    (function(window, $, _) {

        /**
         * Фнукция отправляет ajax запрос для парсинга данных с сервера
         * @private
         */
        var _runDataFetch = function() {
            var dfr = $.Deferred();
            $.ajax('/fetch-avto')
                .done(function(res) {
                    dfr.resolve(res);
                })
                .fail(function(err) {
                    dfr.reject(err);
                });

            return dfr.promise();
        };

        /**
         * Показываем прогресс бар
         * @private
         */
        var _showProgressBar = function() {
            $('.js-fetch-avto-progress-bar').removeClass('app-invisible');
        };

        /**
         * Скрываем прогресс бар
         * @private
         */
        var _hideProgressBar = function() {
            var $el = $('.js-fetch-avto-progress-bar');
            $el.addClass('app-invisible');
        };

        var AvtoDataWidget = function() {};
        AvtoDataWidget.prototype = {
            init: function(app, mods) {
                $('.js-fetch-site-data').on('click', function(e) {
                    _showProgressBar();
                    _runDataFetch()
                        .then(function() {
                            _hideProgressBar();
                            app.reload();
                        }, function() {
                            _hideProgressBar();
                        })
                });
            }
        };
        window.App.register('AvtoDataWidget', new AvtoDataWidget());
    })(window, $, _);


});