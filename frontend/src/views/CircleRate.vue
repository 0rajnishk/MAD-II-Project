<template>
    <NavBar />
    <div class="bg-gradient-to-r from-blue-400 to-purple-300 h-screen flex items-center justify-center max-h-screen">
        <div class="text-center bg-white w-full md:w-3/4 p-4 shadow-gray-600 shadow-lg">
            <h2 class="font-bold text-start mb-4 text-xl">Download circle rate of your city in this list:</h2>
            <div class="overflow-x-auto">
                <table class="min-w-full border border-gray-300">
                    <thead class="bg-blue-500 text-white">
                        <tr>
                            <th class="py-2 px-4">City</th>
                            <th class="py-2 px-4">Official Site</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="py-2 px-4 border border-gray-300">New Delhi</td>
                            <td class="py-2 px-4 border border-gray-300"><a href="eval.delhigovt.nic.in" target="_blank">eval.delhigovt.nic.in</a></td>
                        </tr>
                        <tr>
                            <td class="py-2 px-4 border border-gray-300">Kanpur</td>
                            <td class="py-2 px-4 border border-gray-300"><a href="igrsup.gov.in" target="_blank">igrsup.gov.in</a></td>
                        </tr>
                        <tr>
                            <td class="py-2 px-4 border border-gray-300">Noida</td>
                            <td class="py-2 px-4 border border-gray-300"><a href="gbnagar.nic.in" target="_blank">gbnagar.nic.in</a></td>
                        </tr>
                        <tr>
                            <td class="py-2 px-4 border border-gray-300">Lucknow</td>
                            <td class="py-2 px-4 border border-gray-300"><a href="igrsup.gov.in" target="_blank">igrsup.gov.in</a></td>
                        </tr>
                        <tr>
                            <td class="py-2 px-4 border border-gray-300">Faridabad</td>
                            <td class="py-2 px-4 border border-gray-300"><a href="faridabad.nic.in" target="_blank">faridabad.nic.in</a></td>
                        </tr>
                        <tr>
                            <td class="py-2 px-4 border border-gray-300">Gurgaon</td>
                            <td class="py-2 px-4 border border-gray-300"><a href="gurugram.gov.in" target="_blank">gurugram.gov.in</a></td>
                        </tr>
                        <tr>
                            <td class="py-2 px-4 border border-gray-300">Agra</td>
                            <td class="py-2 px-4 border border-gray-300"><a href="igrsup.gov.in" target="_blank">igrsup.gov.in</a></td>
                        </tr>
                        <tr>
                            <td class="py-2 px-4 border border-gray-300">Dehradun</td>
                            <td class="py-2 px-4 border border-gray-300"><a href="dehradun.nic.in" target="_blank">dehradun.nic.in</a></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <AppFooter />
</template>

<script>
import AppFooter from '../components/AppFooter.vue';
import NavBar from '../components/NavBar.vue';

export default {
    components: {
        NavBar,
        AppFooter,
    },
};

</script>