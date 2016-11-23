(function () {
    "use strict";

    WinJS.UI.Pages.define("/pages/home/home.html", {
        // This function is called whenever a user navigates to this page. It
        // populates the page elements with the app's data.
        ready: function (element, options) {
            
            var titlesListGrouped = new WinJS.Binding.List().createGrouped(
                function (i) { return i.title.charAt(0).toUpperCase(); },
                function (i) { return { firstLetter: i.title.charAt(0).toUpperCase() }; }
            );

            var list = q("#list").winControl;
            list.itemDataSource = titlesListGrouped.dataSource;
            list.itemTemplate = q("#template");
            list.groupDataSource = titlesListGrouped.groups.dataSource;
            list.groupHeaderTemplate = q("#headertemplate");

            WinJS.xhr({ url: "http://odata.netflix.com/Catalog/Titles?$format=json&$top=200" })
                .then(function (xhr) {
                    var titles = JSON.parse(xhr.response).d;
                    titles.forEach(function (i) {
                        titlesListGrouped.push({
                            title: i.ShortName,
                            imageUrl: i.BoxArt.LargeUrl
                        });
                    });
                });

        }
    });
})();
