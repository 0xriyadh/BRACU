#include <stdio.h>

struct Item
{
    int quantity;
    float unit_price;
};

int main()
{
    struct Item paratha, vegetable, mineral_water;
    int num_of_people;
    float total_bill, individual_bill;

    // Input for Paratha
    printf("Quantity Of Paratha: ");
    scanf("%d", &paratha.quantity);
    printf("Unit Price: ");
    scanf("%f", &paratha.unit_price);

    // Input for Vegetables
    printf("Quantity Of Vegetables: ");
    scanf("%d", &vegetable.quantity);
    printf("Unit Price: ");
    scanf("%f", &vegetable.unit_price);

    // Input for Mineral Water
    printf("Quantity Of Mineral Water: ");
    scanf("%d", &mineral_water.quantity);
    printf("Unit Price: ");
    scanf("%f", &mineral_water.unit_price);

    // Input for number of people
    printf("Number of People: ");
    scanf("%d", &num_of_people);

    // Calculate total bill
    total_bill = (paratha.quantity * paratha.unit_price) +
                 (vegetable.quantity * vegetable.unit_price) +
                 (mineral_water.quantity * mineral_water.unit_price);

    // Calculate individual payment
    individual_bill = total_bill / num_of_people;

    // Print the result
    printf("Individual people will pay: %.2f tk\n", individual_bill);

    return 0;
}