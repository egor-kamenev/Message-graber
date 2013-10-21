/**
 * Created with PyCharm.
 * User: e.kamenev
 * Date: 05.02.13
 * Time: 8:50
 * To change this template use File | Settings | File Templates.
 */

///////////////////////////Models////////////////////////////////////
$(function () {


    app.models.Option = Backbone.Model.extend({
            silent: true
        });


    app.models.Message = Backbone.Model.extend({
        silent: true,
        set: function(attrs, options) {

            if ('message_reserve' in attrs) {
                console.log(true);
                this.id = attrs.message_reserve;
            }

            this.prototype.set.apply(this, [attrs, options]);
            return this;
        }

    });

});




