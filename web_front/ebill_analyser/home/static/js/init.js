var fullLineData;
(function ($) {
    $(function () {

        $('.button-collapse').sideNav();
        $('.modal-trigger').leanModal({
            ready: function () {
                drawCallDistro('call-distro-full');
            }
        });
        drawCallDistro('call-distro-mini');
    }); // end of document ready
})(jQuery); // end of jQuery name space

function drawCallDistro(element) {
    var element_id = '#'+element;
    $(element_id).empty();
    Morris.Line({
        element: element,
        data: fullLineData,
        xkey: 'y',
        ykeys: ['a'],
        xLabels: "day",
        axes: true,
        resize: true,
        labels: ['# Calls']
    });
}