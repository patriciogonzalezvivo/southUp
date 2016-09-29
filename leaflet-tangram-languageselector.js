/**
 * Adds a language selector to Leaflet based maps.
 * License: CC0 (Creative Commons Zero), see http://creativecommons.org/publicdomain/zero/1.0/
 * Project page: https://github.com/buche/leaflet-tangram-languageselector
 **/
L.LanguageSelector = L.Control.extend({
    options: {
        languages: {
            // Language selector
            '(default)': false,
            'Arabic': 'ar',
            'German': 'de',
            'English': 'en',
            'Spanish': 'es',
            'French': 'fr',
            'Greek': 'gr',
            'Japanese': 'ja',
            'Russian': 'ru',
            'Korean': 'ko',
            'Chinese': 'zh'
        },
        position: 'topleft',
        scene: null,
        global: ''
    },

    initialize: function(options) {
        L.Util.setOptions(this, options);
    },

    onAdd: function(map) {
        var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom leaflet-tangram-languageselector-container');
        var languageSelector = L.DomUtil.create('SELECT', 'leaflet-tangram-languageselector-selector', container);
        for (var key in this.options.languages) {
            var language = L.DomUtil.create('option', 'leaflet-tangram-languageselector-option');
            if (!this.options.languages[key]) {
                language.text = '(default)';
            }
            else {
                language.text = this.options.languages[key] + ' - ' + key;
            }
            language.value = this.options.languages[key];
            languageSelector.add(language);
        }
        var options = this.options;
        languageSelector.selectedIndex = 3;
        languageSelector.onchange = function(onchange){
            console.log(options)
            console.log('Changing language for', onchange.target.value);
            options.scene.config.global[options.global] = onchange.target.value;
            options.scene.updateConfig();
        }

        return container;
    }
});

L.languageSelector = function(options) { return new L.LanguageSelector(options); };