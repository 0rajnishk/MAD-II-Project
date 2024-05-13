<template>
    <div class="bg-purple-100 p-8 rounded-lg shadow-lg max-w-md mx-auto">
        <!-- Title -->
        <h2 class="text-3xl font-semibold text-purple-800 mb-6">Checkout</h2>

        <!-- Checkout Form -->
        <form>
            <!-- Name on Card Input -->
            <div class="mb-4">
                <label for="nameOnCard" class="block text-purple-800 text-sm font-medium mb-1">
                    Name on Card
                </label>
                <input type="text" id="nameOnCard" name="nameOnCard"
                    class="w-full px-4 py-2.5 border rounded-md focus:outline-none focus:border-purple-500"
                    placeholder="Enter the name on your card" />
            </div>

            <!-- Card Number Input -->
            <div class="mb-4">
                <label for="cardNumber" class="block text-purple-800 text-sm font-medium mb-1">
                    Card Number
                </label>
                <input type="text" id="cardNumber" name="cardNumber"
                    class="w-full px-4 py-2.5 border rounded-md focus:outline-none focus:border-purple-500"
                    placeholder="1111 2222 3333 4444" />
            </div>

            <!-- Expiration Date and CVV Inputs -->
            <div class="flex justify-between mb-4">
                <!-- Expiration Date -->
                <div class="w-1/2 mr-2">
                    <label for="expirationDate" class="block text-purple-800 text-sm font-medium mb-1">
                        Expiration Date
                    </label>
                    <input type="text" id="expirationDate" name="expirationDate"
                        class="w-full px-4 py-2.5 border rounded-md focus:outline-none focus:border-purple-500"
                        placeholder="mm/yy" />
                </div>

                <!-- CVV -->
                <div class="w-1/2 ml-2">
                    <label for="cvv" class="block text-purple-800 text-sm font-medium mb-1">
                        CVV
                    </label>
                    <input type="text" id="cvv" name="cvv"
                        class="w-full px-4 py-2.5 border rounded-md focus:outline-none focus:border-purple-500"
                        placeholder="123" />
                </div>
            </div>

            <!-- Subtotal, Shipping, and Total -->
            <div class="flex justify-between mb-4">
                <!-- Subtotal -->
                <!-- <div>
                    <p class="text-purple-800 text-sm font-medium mb-1">Subtotal</p>
                    <p class="text-purple-800 text-sm font-medium">&#8377;500</p>
                </div> -->

                <!-- Shipping -->
                <!-- <div>
                    <p class="text-purple-800 text-sm font-medium mb-1">Shipping</p>
                    <p class="text-purple-800 text-sm font-medium">&#8377;4</p>
                </div> -->

                <!-- Total -->
                <div>
                    <p class="text-purple-800 text-sm font-medium mb-1">Total (Tax incl.)</p>
                    <p class="text-purple-800 text-sm font-medium">&#8377;1,500</p>
                </div>
            </div>

            <!-- Checkout Button -->
            <div class="flex justify-center">
                <button type="submit" class="bg-purple-800 text-white px-6 py-3 rounded-md font-medium hover:bg-purple-600">
                    Checkout Now
                </button>
            </div>
        </form>
    </div>
</template>
