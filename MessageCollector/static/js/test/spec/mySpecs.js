/**
 * Created with PyCharm.
 * User: e.kamenev
 * Date: 05.02.13
 * Time: 8:33
 * To change this template use File | Settings | File Templates.
 */
$(function () {

describe('Lists',function(){

    /**
     * Получаем данные с сервера и синхронизируем с коллекцией,
     * таким образом избавляемся от дбулирования в тестах коллекций, типа
     * app.collections.List
     *
     * @param  {app.collections.List} collection коллекция для синхронизации
     * @param {number} value_id id модели для присвоения value
     * @param {string} value_name имя поля модели для присвоения его значения value
     */
        var value, flag;
        function fetch_async_collection (collection, value_id, value_name){

            runs(function () {
                flag = false;
                value = '';

                collection.fetch({
                    success: function (collection, data) {
                        value = collection.get(value_id).get(value_name);
                        flag = true;
                    }
                });
            });

            waitsFor(function () {
                return flag;
            }, "Начальные значения не получены", 2000);
        }

    ////////////////////////////////////////////////////////////////////

    /**
     * Инициализируем вид типа app.views.List и возвращаем его
     * @param {app.collections.List} collection коллекця для вида
     * @param {string} el элемент для вила
     * @param {string} value_name название параметра коллекции
     *                  который будет выводиться в шаблоне вида
     * @return {app.views.List} вид
     */
        function init_list_view(collection, el, value_name){

            return new app.views.List({
                el: el,
                collection: collection,
                value_name: value_name
            });

        }

    ////////////////////////////Sources/////////////////////////////////

        describe("Sources", function () {


            it("Инициализация коллекции", function () {

                fetch_async_collection(app.collections.sources, 1 ,'name');

                runs(function () {
                   expect(value).toBe('Diesel');
                });

            });


            it("Инициализация вида", function () {

                app.views.sources = init_list_view(app.collections.sources, '#select-source', 'name');

                expect($('#select-source').children().first().attr('id')).toBe('21');
                expect($('#select-source h5').html()).toBe('Facebook');

            });

            it("getFirstElementId", function(){
                expect(app.views.sources.getFirstElementId()).toBe('21');
            });
        });


    ////////////////////////////Users///////////////////////////////////
        describe("Users", function () {

    /////////
            it("Инициализация коллекции", function () {

                fetch_async_collection(app.collections.users, 1,'login');

                runs(function () {
                    expect(value).toBe('NAFIGATOR');
                });

            });
    /////////

            it("Инициализация вида", function () {

                app.views.users = init_list_view(app.collections.users, '#select-user', 'login');

                expect($('#select-user div').attr('id')).toBe('4');
                expect($('#select-user h5').html()).toBe('угар Винни-Пуха');

            })

        });

        describe('Companions', function () {

            it('Инициализация коллекции', function () {

                fetch_async_collection(app.collections.companions, 1,'name');

                runs(function () {
                    expect(value).toBe('NAFIGATOR');
                });

            });


            it('Инициализация вида', function () {

                app.views.companions = init_list_view(app.collections.companions, "#select-companion", 'name');

                expect($('#select-companion div').attr('id')).toBe('1');
                expect($('#select-companion h5').html()).toBe('NAFIGATOR');


            });

        });

        //TODO инициализация коллекции
        describe('Messages', function() {

            it('Инициализация коллекции', function(){
                runs(function () {
                    flag = false;
                    value = '';

                    app.collections.messages.fetch({
                        success: function (collection, data) {
                            console.log(collection.model);

                            value = collection.get(44).get('text');
                            flag = true;
                        }
                    });
                });

                waitsFor(function () {
                    return flag;
                }, "Начальные значения не получены", 2000);

                runs(function(){
                    expect(value).toContain('Оригинальные моторные и трансмиссионные масла из США(Honda, Subaru, Toyota)');
                })
            });



        });




    });

});