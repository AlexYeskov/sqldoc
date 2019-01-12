$(function(){

function indexOf(obj, list) {
    var i;
    for (i = 0; i < list.length; i++) {
        if (JSON.stringify(list[i]) == JSON.stringify(obj))
            return i;
    }
    return -1;
}
function getUnique(value, index, self) {
    return self.indexOf(value) === index;
}
var selectedColumns = [];
var statement = '';

$('body').on("click",".sqldocs-select input",function(e){
    e.stopPropagation();
    thisColumn = {
         tbl: $(this).attr("name")
        ,col: $($(this).parent().parent().find('.sqldocs-colname')).text()
    }

    thisIndex = indexOf(thisColumn,selectedColumns);

    if (this.checked && thisIndex==-1)
        selectedColumns.push(thisColumn);
    else if (thisIndex!=-1)
        selectedColumns.splice(thisIndex,1);

    tableList = (selectedColumns.map(function(a) {return 'analytics.'+a.tbl;})).filter(getUnique);

    if (selectedColumns.length>0) {
        statement = 'SELECT '+selectedColumns.map(function(a) {return '<span class="sqldocs-comment">,'+a.col+'</span>';}).join('');
        if (tableList.length==1)
            statement += '<span class="sqldocs-comment">FROM '+tableList[0]+'</span>';
        else
            statement += '<span class="sqldocs-comment">FROM '+tableList.join(', ')+'</span><span class="sqldocs-comment">WHERE /*JOIN CONDITION*/</span>';
        statement += '<span class="sqldocs-comment">LIMIT 1</span>';
    } else
        statement = '';

    $('#sqlpopup').html(statement);
    $($('#sqlpopup').find('span')[0]).html($($('#sqlpopup').find('span')[0]).html().replace(',',' '));
    $("#sqlpopup").css({top: 50,left: $('body').width()/4,zIndex: 50});
    $("#sqlpopup").show();
  });

  $("#sqlpopup").click(function(e){
      document.execCommand("copy");
      $("#sqlpopup").hide();
  });
  $("body").click(function(e){
      if ($("#sqlpopup").css("display")!="none")
          $("#sqlpopup").hide();
  });

  $("body").scroll(function(e){
    $("#sqlpopup").hide();
  });
});