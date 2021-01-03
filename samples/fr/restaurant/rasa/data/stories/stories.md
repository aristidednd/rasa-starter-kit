## welcome
* greet
  - utter_greet

##  goodbye
* goodbye
  - utter_see_you_soon

## happy restaurant path
* greet
  - utter_greet
* book_a_place
  - booking_form
  - form{"name": "booking_form"}
  - form{"name": null}
  - utter_acknowledge_informations
  - utter_summarize_booking
* goodbye
  - utter_see_you_soon
