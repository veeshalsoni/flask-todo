
$(document).ready(function() {

	var datatable = $('#tasktable').DataTable();

	$("#tasktable tbody").on("click","button[id^=task-done]",function(event){
		$(this).toggleClass("task-done");
		var tid = $(this).attr('id');
		$.post("/taskcompleted",{
			"id" : tid
		},function(data){
			$('#taskops').text(data.status).show();
		});
	});


	$("button[id^=task-delete]").on('click',function(event){
		var tid = $(this).attr('id');
		$.post("/deletetask",{
			"id" : tid
		},function(data){
			$('#taskops').text(data.status).show();
		});
			datatable.row($(this).parents("tr")).remove().draw(false)

	});

	$('#taskform').on('submit', function(event) {

		$.ajax({
			data : {
				text : $('#text').val(),
				category : $('#category').val(),
				taskdate : $('#taskdate').val()
			},
			type : 'POST',
			url : '/addtask'
		})
		.done(function(data) {

			if (data.Error) {
				$('#taskinfo').text(data.Error).show();
			}
			else {
				$('#taskinfo').text(data.Success).show();
				var text = $('#text').val();
				var category = $('#category').val();
				var taskdate = $('#taskdate').val();
				var showdate = $("#date").val();
				$("#text").val("");
				$('#category').val("");

				if (showdate == taskdate)
				{
					markup = '<tr> <td class="col-md-3">' + category + '</td> <td class="col-md-7">' + text + '</td> <td class="col-md-1"> <button id = "task-done-'+ (data.id).toString() +'" class="btn btn-default btn-sm glyphicon glyphicon-check"> </button> </td> <td class="col-md-1"> <button id = "task-delete-'+ (data.id).toString() +'" class="btn btn-default btn-sm glyphicon glyphicon-remove" style="color:red"> </button> </td> </tr>'
					datatable.row.add($(markup)).draw(false)
				}
			}
		});
		event.preventDefault();
	});
});