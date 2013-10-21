/**
 * Created with PyCharm.
 * User: e.kamenev
 * Date: 12.02.13
 * Time: 10:29
 * To change this template use File | Settings | File Templates.
 */

$(function () {
    app.collections.sources = new app.collections.List({
        url: '/sources/'
    });

    app.collections.users = new app.collections.List({
        url: '/users/',
        data:{
            source_id: 1
        }
    });

    app.collections.companions = new app.collections.List({
        url: '/companions/',
        data:{
            source_user_id: 1
        }
    });

    app.collections.messages = new app.collections.List({
        url: '/messages/',
        data:{
            companion_id: 1
        },
        model: app.models.Message
    });


});