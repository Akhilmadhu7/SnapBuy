$(document).ready(function () {
   
    console.log('sdhfiashdfihfkasnilash');
    $('.paywithrazorpay').click(function (e){
        console.log('sdhfiashdfihfkasnilash');
        e.preventDefault();
        console.log('sdhfiashdfihfkasnilash');
        var customername = $("[name = 'name']").val();
        var phone = $("[name = 'phone']").val();
        var email = $("[name = 'email']").val();
        var address = $("[name = 'address']").val();
        var pincode = $("[name = 'pincode']").val();
        var state = $("[name = 'state']").val();
        var city = $("[name = 'city']").val();
        var country = $("[name = 'country']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();
        
        

        if(customername == "" || email == "" || phone == "" || address == "" || pincode == "" || 
            state == "" || city == "" || country == "") 
        
            {
                swal("Alert!", "All fields are mandatory!", "error");

                return false;

            }
        else
        {  
            $.ajax({
                
                method: "GET",
                url: "/newcart/proceed-to-pay",
                success: function (response) {
                    

                    var options = {
                        "key": "rzp_test_0SSIYnAjylsV83", // Enter the Key ID generated from the Dashboard
                        "amount": parseInt(response.grandtotal * 0.01), // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "Acme Corp",
                        "description": "Test Transaction",
                        "image": "https://example.com/your_logo",
                        // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (responseb){
                            alert(responseb.razorpay_payment_id);

                            data = {

                                "name": customername,
                                "phone": phone ,
                                "email": email ,
                                "address": address,
                                "pincode": pincode,
                                "state": state, 
                                "city": city ,
                                "country": country,
                                "paymentmode": "paid by razorpay",
                                "payment_id" : responseb.razorpay_payment_id,
                                csrfmiddlewaretoken : token
                            }
                            
                            $.ajax({
                                
                                method: "POST",
                                url: "/newcart/place-order",
                                data: data,
                                
                                success: function (responsec){
                                    swal("Congratulations!",responsec.status, "success").then((value) => {
                                        window.location.href = '/newcart/invoice'
                                      });

                                }
                            })
                            
                        },
                        "prefill": {
                            "name": customername,
                            "email": email,
                            "contact": phone
                        },
                        
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();

                }
            }) ;

           
        }    


        

    });
});


