function dtStart(ajax, config) {
    /* Function for start DataTables with option for server side mode
    * :param: api_url [string]: URL for the api
    * :param: config[array]: objects arry for  extra parameters for specific column, OPTIONAL*/

    var configuration = config || [
        {
            orderable: true,
            searchable: true,
            className: "center",
            targets: [0, 1]
        }
    ];
    $('.datatable').dataTable({
        order: [[0, "desc"]],
        lengthMenu: [[5, 10, 20, 100], [5, 10, 20, 100]],
        columnDefs: configuration,
        searching: true,
        processing: true,
        serverSide: true,
        stateSave: true,
        ajax: ajax,
        "pagingType": "full_numbers",
        dom:
        "<'ui two column grid'<'left aligned column'l><'right aligned column'f>>" +
        "<'ui grid'<'column'tr>>" +
        "<'ui two column grid'<'left aligned column'i><'right aligned column'p>>"
    });
}