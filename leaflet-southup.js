var southUp = function(map){
    // Disble and over right behaviur of a map
    map.options.scrollWheelZoom = 'center';
    map.options.doubleClickZoom = 'center';
    map.boxZoom.disable();
    map.dragging.disable();

    // Overload Mouse events to invert them
    var prevPoint = undefined;
    map._container.addEventListener('mousedown', function (event) {
        var first = event.touches ? event.touches[0] : event;
        prevPoint = new L.Point(first.clientX, first.clientY);
    }, false);
    map._container.addEventListener('mousemove', function (event) {
        if (prevPoint) {
            var first = event.touches ? event.touches[0] : event;
            var newPoint = new L.Point(first.clientX, first.clientY);
            var offset = newPoint.subtract(prevPoint);
            prevPoint = newPoint;
            map.panBy(offset, {animate: false});
        }
    }, false);
    map._container.addEventListener('mouseup', function (event) {
        prevPoint = undefined;
    }, false);
    map._container.addEventListener('mouseout', function (event) {
        prevPoint = undefined;
    }, false);
    map._container.addEventListener('mouseleave', function (event) {
        prevPoint = undefined;
    }, false);
};