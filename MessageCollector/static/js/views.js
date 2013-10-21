/**
 * Created with PyCharm.
 * User: e.kamenev
 * Date: 05.02.13
 * Time: 8:58
 * To change this template use File | Settings | File Templates.
 */

///////////////////////////Views////////////////////////////////////

$(function(){

////////////////////////////List////////////////////////////////////

    app.views.List = Backbone.View.extend({

        template: _.template($('#list-template').html()),

        events:{
            'click div.select' : 'updateList',
        },

        initialize: function () {
            _.bindAll(this,
                'render',
                'remove',
                'publish',
                'getFirstElementId',
                'selected',
                'unselectAll',
                'updateList'
            );

            this.render();
        },

        render: function () {
            var temp = this.template({
                sources: this.collection,
                value_name: this.options.value_name
            });
            this.$el.append(temp);
            return this;
        },

        // т.к. два события на один элемент в events вешать нельзя,
        // используем отдельный метод
        updateList: function(event){
            this.publish(event);
            this.selected(event);
        },

        remove: function () {
            this.$el.html('');
        },

        // сообщаем через посредника о новом выбранном элементе списка
        publish: function (event) {
            this.options.mediator.publish(this.options.channel,$(event.target).attr('id'));
        },

        getFirstElementId: function () {

            return this.$el.children().first().attr('id');

        },

        selected: function (event) {
            this.unselectAll();

            //Выбераем ближайший DIV, если ткнули на внутренний элемент
            var target = (event.target.tagName == 'DIV') ? event.target : $(event.target).parent();
            $(target).addClass('green');
        },

        unselectAll: function (event) {

            _.each(this.$el.children(), function(value, index){
                $(this.$el.children()[index]).removeClass('green');
            }, this );

        }

    });

/////////////////////////Messenger//////////////////////////////////
//    app.views.Messages = Backbone.View.extend({
//
//    });


});