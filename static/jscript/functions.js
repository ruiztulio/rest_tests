
get_products = function ()
{
	var resp = jQuery.getJSON('products/', function(response) 
	{
		var html = "<table><tr><th>Descripci&oacute;n</th></tr>";
		for(var i=0; i < response.products.length; ++i)
			html += "<tr><td width=\"100\">"+response.products[i].name+"</td>"+
					"<td width=\"40\" align=\"right\">"+response.products[i].price+"</td>"+
					"<td width=\"40\" >"+response.products[i].quantity+"</td>"+
					"<td width=\"40\" >"+response.products[i].code+"</td></tr>";
		html += "</table>";
		jQuery("#products").html(html);
	});
}

get_sales = function (href)
{
	var resp = jQuery.getJSON(href, function(response) 
	{
		var html = "<table><tr><th>Cliente</th><th>Detalle</th><th>Fecha</th></tr>";
		for(var i=0; i < response.sales.length; ++i)
			html += "<tr><td width=\"100\"><a href=\""+response.sales[i].client_id_ref+"\" class=\"client-link\">"+ response.sales[i].client_name+"</a></td>"+
					"<td width=\"100\"><a href=\""+response.sales[i].detail_ref+"\" class=\"detail-link\">Detalle</a></td>"+
					"<td width=\"100\" align=\"right\">"+response.sales[i].sale_date+"</td></tr>";
		html += "</table>";
		jQuery("#sales").html(html);
	});
}

get_clients = function (url)
{
	var resp = jQuery.getJSON(url, function(response) 
	{
		var html = "<table><tr><th>Cliente</th><th>RIF</th><th>Tel&eacute;fono</th><th>Direcci&oacute;n</th></tr>";
		for(var i=0; i < response.clients.length; ++i)
			html += "<tr><td width=\"100\">"+response.clients[i].name+"</td>"+
					"<td width=\"100\" align=\"right\">"+response.clients[i].vat+"</td>"+
					"<td width=\"100\" align=\"right\">"+response.clients[i].phone+"</td>"+
					"<td width=\"150\" align=\"right\">"+response.clients[i].address+"</td></tr>";
		html += "</table>";
		jQuery("#clients").html(html);
	});
}

get_detail = function (url)
{
	var resp = jQuery.getJSON(url, function(response) 
	{
		var html = "<table><tr><th>Producto</th><th>Cantidad</th><th>Precio unitario</th></tr>";
		for(var i=0; i < response.detail.length; ++i)
			html += "<tr><td width=\"100\">"+response.detail[i].product_name+"</td>"+
					"<td width=\"100\" align=\"right\">"+response.detail[i].quantity+"</td>"+
					"<td width=\"100\" align=\"right\">"+response.detail[i].price+"</td></tr>";
		html += "</table>";
		jQuery("#detail").html(html);
	});
}
