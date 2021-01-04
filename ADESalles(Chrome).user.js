// ==UserScript==
// @name           ADESalles(Chrome)
// @version        1.0.4
// @author         Antoine-Alexis BOURDON
// @license        GPL version 3 or any later version; http://www.gnu.org/copyleft/gpl.html
// @include        http://ade-consult.univ-artois.fr/*
// @Description    Version 1.0.4, la 3 nous met directement sur l'edt M1 , la 4 met le display sur etudiants par défaut
// ==/UserScript==

var nom = window.document.URL;

if (nom.includes("myplanning.jsp")){
    window.location.replace("http://ade-consult.univ-artois.fr/direct/index.jsp?resources=9085,9465&displayConfName=ETUDIANTS-ENT");
}


var open_prototype = XMLHttpRequest.prototype.open,
intercept_response = function(urlpattern, callback) {
   XMLHttpRequest.prototype.open = function() {
      arguments['1'].match(urlpattern) && this.addEventListener('readystatechange', function(event) {
         if ( this.readyState === 4 ) {
            var response = callback(event.target.responseText);
            Object.defineProperty(this, 'response', {writable: true});
            Object.defineProperty(this, 'responseText', {writable: true});
            this.response = this.responseText = response;
         }
      });
      return open_prototype.apply(this, arguments);
   };
};

intercept_response(/DirectPlanningServiceProxy/i, function(response) {
   var new_response = response.replace("//OK[1,[\"{\\\"0\\\"{\\\"-100\\\"\\\"true\\\"\\\"-1\\\"\\\"1\\\"\\\"0\\\"\\\"0\\\"\\\"0\\\"\\\"false\\\"[0]\\\"\\\"\\\"\\\"\\\"0\\\"\\\"0\\\"[0][0][1]{\\\"-7\\\"\\\"true\\\"\\\"0\\\"\\\"-1\\\"\\\"0\\\"\\\"0\\\"\\\"0\\\"\\\"false\\\"[1]{\\\"StringField\\\"\\\"NAME\\\"\\\"LabelName\\\"\\\"type.Category7\\\"\\\"false\\\"\\\"false\\\"\\\"\\\"\\\"category7\\\"\\\"7\\\"\\\"0\\\"[0][0]\\\"false\\\"\"],0,7]","//OK[1,[\"{\\\"0\\\"{\\\"-100\\\"\\\"true\\\"\\\"-1\\\"\\\"8\\\"\\\"0\\\"\\\"7\\\"\\\"0\\\"\\\"false\\\"[0]\\\"\\\"\\\"\\\"\\\"0\\\"\\\"0\\\"[0][0][8]{\\\"-1\\\"\\\"true\\\"\\\"0\\\"\\\"-1\\\"\\\"0\\\"\\\"0\\\"\\\"0\\\"\\\"false\\\"[1]{\\\"StringField\\\"\\\"NAME\\\"\\\"LabelName\\\"\\\"type.Category1\\\"\\\"false\\\"\\\"false\\\"\\\"\\\"\\\"trainee\\\"\\\"1\\\"\\\"0\\\"[0][0]{\\\"-2\\\"\\\"true\\\"\\\"0\\\"\\\"-1\\\"\\\"1\\\"\\\"1\\\"\\\"0\\\"\\\"false\\\"[1]{\\\"StringField\\\"\\\"NAME\\\"\\\"LabelName\\\"\\\"type.Category2\\\"\\\"false\\\"\\\"false\\\"\\\"\\\"\\\"instructor\\\"\\\"2\\\"\\\"0\\\"[0][0]{\\\"-3\\\"\\\"true\\\"\\\"0\\\"\\\"-1\\\"\\\"2\\\"\\\"2\\\"\\\"0\\\"\\\"false\\\"[1]{\\\"StringField\\\"\\\"NAME\\\"\\\"LabelName\\\"\\\"type.Category3\\\"\\\"false\\\"\\\"false\\\"\\\"\\\"\\\"classroom\\\"\\\"3\\\"\\\"0\\\"[0][0]{\\\"-4\\\"\\\"true\\\"\\\"0\\\"\\\"-1\\\"\\\"3\\\"\\\"3\\\"\\\"0\\\"\\\"false\\\"[1]{\\\"StringField\\\"\\\"NAME\\\"\\\"LabelName\\\"\\\"type.Category4\\\"\\\"false\\\"\\\"false\\\"\\\"\\\"\\\"equipment\\\"\\\"4\\\"\\\"0\\\"[0][0]{\\\"-5\\\"\\\"true\\\"\\\"0\\\"\\\"-1\\\"\\\"4\\\"\\\"4\\\"\\\"0\\\"\\\"false\\\"[1]{\\\"StringField\\\"\\\"NAME\\\"\\\"LabelName\\\"\\\"type.Category5\\\"\\\"false\\\"\\\"false\\\"\\\"\\\"\\\"category5\\\"\\\"5\\\"\\\"0\\\"[0][0]{\\\"-6\\\"\\\"true\\\"\\\"0\\\"\\\"-1\\\"\\\"5\\\"\\\"5\\\"\\\"0\\\"\\\"false\\\"[1]{\\\"StringField\\\"\\\"NAME\\\"\\\"LabelName\\\"\\\"type.Category6\\\"\\\"false\\\"\\\"false\\\"\\\"\\\"\\\"category6\\\"\\\"6\\\"\\\"0\\\"[0][0]{\\\"-7\\\"\\\"true\\\"\\\"0\\\"\\\"-1\\\"\\\"6\\\"\\\"6\\\"\\\"0\\\"\\\"false\\\"[1]{\\\"StringField\\\"\\\"NAME\\\"\\\"LabelName\\\"\\\"type.Category7\\\"\\\"false\\\"\\\"false\\\"\\\"\\\"\\\"category7\\\"\\\"7\\\"\\\"0\\\"[0][0]{\\\"-8\\\"\\\"true\\\"\\\"0\\\"\\\"-1\\\"\\\"7\\\"\\\"7\\\"\\\"0\\\"\\\"false\\\"[1]{\\\"StringField\\\"\\\"NAME\\\"\\\"LabelName\\\"\\\"type.Category8\\\"\\\"false\\\"\\\"false\\\"\\\"\\\"\\\"category8\\\"\\\"8\\\"\\\"0\\\"[0][0]\\\"false\\\"\"],0,7]");
   return new_response;
});

