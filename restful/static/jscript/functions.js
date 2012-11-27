
get_products = function ()
{
	var resp = jQuery.getJSON('products', function(response) 
	{
		var html = "<table><tr><th>Descripci&oacute;n</th><th>Precio</th><th>Cantidad</th><th>C&oacute;digo</th></tr>";
		for(var i=0; i < response.products.length; ++i)
			html += "<tr><td width=\"100\">"+response.products[i].name+"</td>"+
					"<td width=\"40\" align=\"right\">"+response.products[i].price+"</td>"+
					"<td width=\"40\" >"+response.products[i].quantity+"</td>"+
					"<td width=\"40\" >"+response.products[i].code+"</td></tr>";
		html += "</table>";
		jQuery("#products").html(html);
        jQuery("#response").append("get_products " +response.status.id + " : " +  response.status.message+"<br />");
	});
}

get_products_delete = function ()
{
	var resp = jQuery.getJSON('products', function(response) 
	{
        var html = "<form name=\"product_delete\" id=\"product_delete\""+ 
                    "action=\"javascript:send_form('product_delete', 'delete', 'products', 'delete_products')\""+
                    "method=\"post\" >";

		html += "<table><tr><th></th><th>Descripci&oacute;n</th><th>Precio</th><th>Cantidad</th><th>C&oacute;digo</th></tr>";
		for(var i=0; i < response.products.length; ++i)
			html += "<tr><td><input type=\"radio\" name=\"id\" value=\"" +response.products[i].id + "\"></td>"+
                    "<td width=\"100\">"+response.products[i].name+"</td>"+
					"<td width=\"40\" align=\"right\">"+response.products[i].price+"</td>"+
					"<td width=\"40\" >"+response.products[i].quantity+"</td>"+
					"<td width=\"40\" >"+response.products[i].code+"</td></tr>";
		html += "</table><INPUT class=\"btn\" type=\"submit\" value=\"Delete\" id=\"submit\"></form>";
		jQuery("#products").html(html);
        jQuery("#response").append("get_products " +response.status.id + " : " +  response.status.message+"<br />");
	});
}

send_form = function (form, type, url, action, callback=null)
{
    var datos   = '';
    var dataVal = '';

    jQuery('#'+form+' :input').each(
    
        function() 
        {
            value = '';
            dataVal = '';
            if(this.type == 'checkbox')
            {
                if(this.checked)
                {
                    value   = this.value!='' ? this.value : 'on';
                        dataVal = this.name+'='+value+'&'
                }
            }
            else if(this.type == 'radio')
            {
                if(this.checked)
                {
                    value   = this.value!='' ? this.value : 'on';
                    dataVal = this.name+'='+value+'&'
                }
            }
            else if (this.name != "")
            {
                value   = this.value;
                dataVal = this.name+'='+value+'&';
            }
            datos   = datos + dataVal;
        }
    );
    jQuery.ajax({
        type       : type,
        url        : url,
        data       : datos,
        dataType   : 'json',
        cache      : false,
        success    : function (response) 
        {
            if (callback)
                callback();
            jQuery("#response").append(action +" " +response.status.id + " : " +  response.status.message+"<br />");
        }
    });


}
