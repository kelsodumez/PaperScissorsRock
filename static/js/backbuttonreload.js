/** https://stackoverflow.com/questions/43043113/how-to-force-reloading-a-page-when-using-browser-back-button
  * Click a grade, change the grade, click back - page does not show the changes
  * so this forces a page reload if the 'BACK' button is used to load the page
  **/
 window.addEventListener("pageshow", function (event) {
    var perfEntries = performance.getEntriesByType("navigation");
    if (perfEntries[0].type === "back_forward") {
        location.reload(true);
    }
  });