function stateFilter() {
    var state_selector = document.getElementById("state-selector");
    var state = state_selector.options[state_selector.selectedIndex].value;

    window.location = "/order/admin/1/" + state;
}
