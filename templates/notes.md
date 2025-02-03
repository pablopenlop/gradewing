Raises an error that stops the form's validation and renders the error for the entire form or a specific field.

raise forms.ValidationError({
    "end_date": "End date cannot be earlier than the start date."
})


if form.is_valid():
        print("success")
        form.save()
        messages.success(request, 'Academic Period added successfully!')
        return JsonResponse({
            'success': True, 
            'redirect': reverse('periods')
        }) 
together with
$(document).ready(function() {
    $(document).on('submit', '#add-period-form', function(event) {
        event.preventDefault(); 

        var form = $(this);
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                console.log(response); 
                
                if (response.success) {
                    console.log('Form submitted successfully, redirecting.');
                    window.location.href = response.redirect; 
                } else {
                    console.log('Form submission failed, updating form content.');
                    $('#period-form_container').html(response.html);
                }
            },
            error: function(xhr, status, error) {
                console.log('AJAX request error:', error); // Handle errors here
            }

        });
    });
});


<div class="col-lg d-flex flex-column flex-lg-row justify-content-between align-items-center">
<div class="col-lg d-flex flex-column flex-lg-row justify-content-between align-items-center">



    class StudentPeriodForm(forms.ModelForm):
    id = forms.IntegerField(
        widget=forms.HiddenInput(), 
        required=False
    )
    programmes = forms.MultipleChoiceField(
        choices=QF.grouped_choices(),
        widget= forms.SelectMultiple(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
    )


    class StudentPeriod(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="periods")
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name="students")
    yeargroup = models.CharField(
        max_length=10,
        choices=Yeargroup.grouped_choices(),
    )
    programmes = models.JSONField(blank=True, null=True, default=list)

    def get_programmes(self):
        return QF.choices_from_values(self.programmes)

        {% for programme in period.get_programmes %} 
        <span class="badge mb-1">{{programme.label}}</span>
        {% endfor %}








    {% comment %} <style>
        /* Container */
        .step-progress {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 80%;
            margin: 20px auto;
            position: relative;
        }



        .step {
            position: relative;
            z-index: 1;
            text-align: center;
            flex: 1;
        }

        .step-number {
            width: 30px;
            height: 30px;
            background: #e0e0e0;
            color: #777;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin: 0 auto 10px;
        }

        .step.active .step-number {
            background:rgb(190, 210, 230);
            color: rgb(44, 101, 216); 
        }

        .step.complete .step-number {
            background:rgb(190, 210, 230);
            color: rgb(44, 101, 216); 
        }

        .step-title {
            font-size: 14px;
            font-weight: bold;
            color: #333;
        }

        .step-desc {
            font-size: 12px;
            color: #777;
        }

        /* Active step line */
        .step.complete::before {
            content: "";
            position: absolute;
            top: 15px;
            left: 50%;
            height: 3px;
            background:rgb(190, 210, 230);
            width: 100%;
            z-index: -1;
        }

    </style>


    <div class="step-progress">
        <!-- Step 1 -->
        <div class="step complete">
            <div class="step-number">01</div>
            <!--<div class="step-desc">Academic period</div>-->
        </div>
        <!-- Step 2 -->
        <div class="step active">
            <div class="step-number">02</div>
            <!--<div class="step-desc">Subject</div>-->
        </div>
        <!-- Step 3 -->
        <div class="step">
            <div class="step-number">03</div>
           <!-- <div class="step-desc">Members</div>-->
        </div>
    </div>
 {% endcomment %}


 <script src="{% static 'components/countryselect/js/countrySelect.js' %}"></script>
<link href="{% static 'components/countryselect/css/countrySelect.css' %}" rel="stylesheet"> 



 <div class="card"> 
    <div class="card-header">
        School
    </div>
    <div class="card-body">
        <form>
            <label for="country_selector">Country.</label>
            <div class="form">
                <input class="form-control" id="country_selector" type="text">
                
            </div>
            <div class="form-item" style="display:;">
                <input type="text" id="country_selector_code" name="country_selector_code" data-countrycodeinput="1" readonly="readonly" placeholder="Selected country code will appear here" />
                <label for="country_selector_code">...and the selected country code will be updated here</label>
            </div>
            <button type="submit" style="display:none;">Submit</button>
        </form>

        <!-- Load jQuery from CDN so can run demo immediately -->
        <script>
            $("#country_selector").countrySelect({
                defaultCountry: "gb",
                // onlyCountries: ['us', 'gb', 'ch', 'ca', 'do'],
                responsiveDropdown: false,
                preferredCountries: ['gb', 'es']
            });
        </script>
    </div>
    <div class="card-body">
        School
    </div>
    <div class="card-body">
        School
    </div>
</div>