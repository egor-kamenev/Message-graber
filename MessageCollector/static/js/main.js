/*
 * Created with PyCharm.
 * User: e.kamenev
 * Date: 25.01.13
 * Time: 15:45
 * To change this template use File | Settings | File Templates.
 */

$(function() {


///////////////////////////Init////////////////////////////////////
    // Объект посредник
    var mediator = new Mediator();




//Sources
    app.collections.sources.fetch({
        url: '/sources/',
        success: function (collection, data) {
            app.views.sources = new app.views.List({
                el: "#select-source",
                mediator: mediator,
                channel: "list:source:change",
                collection: collection,
                value_name: 'name'
            });
        }
    });




//Users

    app.collections.users.fetch({
        data: {
            source_id: 1
        },
        url: '/users/',
        success: function (collection, data) {
            app.views.users = new app.views.List({
                el: "#select-user",
                mediator: mediator,
                collection: collection,
                channel: "list:user:change",
                value_name: 'login'
            });

        }

    });

    mediator.subscribe("list:source:change",function(id){

        app.collections.users.fetch({
            data: {
                source_id: id
            },

            success: function (collection, data) {
                app.views.users.remove();
                app.views.users.render();
                mediator.publish('list:user:change', app.views.users.getFirstElementId());
            }
        });
    });


//Companion
    app.collections.companions.fetch({

        data:{
            source_user_id :1
        },

        url: '/companions/',

        success: function (collection, data) {
            app.views.companions = new app.views.List({
                el: "#select-companion",
                mediator: mediator,
                channel: "list:companion:change",
                collection: app.collections.companions,
                value_name: 'name'
            });
        }


    });

    mediator.subscribe("list:user:change",function(id){

        app.collections.companions.fetch({

            data: {
                source_user_id: id
            },

            success: function (collection, data) {
                app.views.companions.remove();
                app.views.companions.render();
            },

            error: function(collection, data){
                app.views.companions.remove();
            }

        });
    });



});



