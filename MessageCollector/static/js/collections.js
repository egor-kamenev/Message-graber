/**
 * Created with PyCharm.
 * User: e.kamenev
 * Date: 05.02.13
 * Time: 8:55
 * To change this template use File | Settings | File Templates.
 */

///////////////////////////Collections////////////////////////////////////


$(function () {

//////////////////////////////////////////////////////////////////////////

    app.collections.List = Backbone.Collection.extend({
        model: app.models.Option,

        initialize: function(options) {
            /*
            * инициализируем данные переменные
            * т.к. по умолчанию они не инизиализируются,
            * эти данные необходимы при синхронизации коллекции
            */
            this.url = options.url;
            this.data = options.data;
        },

        sync: function(method, collection, options){
            /*
                Складываем все опции необходимые для синхронизации в один объект,
                для того чтобы иметь возможность задавать различные данные
                при описании, создании, и синхронизации коллекции

           */

            var opt = $.extend({},{
                url: collection.url,
                data: collection.data
            }, options);

            switch (method){
                case 'read' : return Backbone.sync(method, collection, opt);
                break;

                case 'create' :case 'update' :case 'delete':
                    return Backbone.sync(method, collection, options);
                break;
            }

        }
    });

//////////////////////////////////////////////////////////////////////////

    app.collections.Message = Backbone.Collection.extend({
        model: app.models.Message,

        initialize: function(options) {
            /*
             * инициализируем данные переменные
             * т.к. по умолчанию они не инизиализируются,
             * эти данные необходимы при синхронизации коллекции
             */
            this.url = options.url;
            this.data = options.data;
        },

        sync: function(method, collection, options){
            /*
             Складываем все опции необходимые для синхронизации в один объект,
             для того чтобы иметь возможность задавать различные данные
             при описании, создании, и синхронизации коллекции

             */

            var opt = $.extend({},{
                url: collection.url,
                data: collection.data
            }, options);

            switch (method){
                case 'read' : return Backbone.sync(method, collection, opt);
                    break;

                case 'create' :case 'update' :case 'delete':
                return Backbone.sync(method, collection, options);
                break;
            }

        }
    });





});