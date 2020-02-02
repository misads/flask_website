function htmlentities(string) {
    return $('<div/>').text(string).html();
}

function ezq(args){
    // {#var res = modal.format(args.title, args.body);#}
    var res = '<div class="modal fade" tabindex="-1" role="dialog">' +
    '  <div class="modal-dialog" role="document">' +
    '    <div class="modal-content">' +
    '      <div class="modal-header">' +
    '        <span class="f-12">' + args.title + '</span>' +
    '        <button type="button" class="close" data-dismiss="modal" aria-label="Close">' +
    '          <span aria-hidden="true">&times;</span>' +
    '        </button>' +
    '      </div>' +
    '      <div class="modal-body">' +
    '        <p>' + args.body + '</p>' +
    '      </div>' +
    '      <div class="modal-footer">' +
    '      </div>' +
    '    </div>' +
    '  </div>' +
    '</div>';
    var obj = $(res);
    var deny = '<button type="button" class="btn btn-danger" data-dismiss="modal">取消</button>';
    var confirm = $('<button type="button" class="btn btn-primary" data-dismiss="modal">确定</button>')

    obj.find('.modal-footer').append(deny);
    obj.find('.modal-footer').append(confirm);

    $('main').append(obj);

    $(obj).on('hidden.bs.modal', function (e) {
        $(this).modal('dispose');
    });

    $(confirm).click(function(){
        args.success();
    });

    obj.modal('show');

    return obj;
}

