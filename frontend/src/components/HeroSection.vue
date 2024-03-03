<template>
  <div class="h-screen flex items-center justify-center hero-bg bg-cover bg-center"
    :style="{ backgroundImage: `url(${backgroundImage})` }">
    <div class="items-stretch flex max-w-[976px] flex-col">
      <div class=" gradient-txt text-xl font-bold leading-6 tracking-tight bg-clip-text self-center whitespace-nowrap">
        Adopt Trees with Confidence
      </div>

      <div
        class="text-green-800  text-center text-6xl font-bold leading-[70px] tracking-tighter w-full mt-12 max-md:max-w-full max-md:text-4xl max-md:leading-10 max-md:mt-10">
        &quot;Embrace a Greener Tomorrow: Adopt a Tree Today and Nurture Nature for a Sustainable Future!&quot;
      </div>
      <router-link to="/adopt"
        class="text-center text-2xl font-bold tracking-tighter w-full mt-12 max-md:max-w-full max-md:text-0.2xl max-md:leading-1 max-md:mt-10">
        <button
          class="text-white font-bold mt-12 mb-12 border-white border-4 p-2 pl-6 pr-6 rounded-2xl bg-gradient-to-r from-green-600 to-pink-600">
          Click Here to Proceed Adopting Trees
        </button>
      </router-link>

    </div>
  </div>

  <br>

  <div class="justify-center items-stretch bg-green-700 flex flex-col py-2 rounded-[70px] lg:mx-8">
    <div
      class="items-center bg-purple-50 flex flex-col pt-8 pb-3 px-16 rounded-[60px] max-md:max-w-[800px] max-md:mr-0.5 max-md:px-5">
      <div class="flex w-[810px] max-w-full flex-col items-stretch">
        <div class="text-black text-center lg:text-4xl font-bold self-center whitespace-nowrap max-md:max-w-full">
          Adopt a Tree in Three Simple Steps
        </div>
        <div
          class="text-neutral-400 text-center text-base font-medium leading-6 self-center w-full mt-7 max-md:max-w-full">
          "Embark on a journey of eco-consciousness with our Adopt a Tree initiative. Our platform guarantees a
          hassle-free and time-saving experience, ensuring a cost-effective and corruption-free adoption process. Join us
          in fostering a greener future through authentic and efficient tree adoptions."
        </div>
        <div class="mt-8 max-md:max-w-full">
          <div class="gap-5 flex max-md:flex-col max-md:items-stretch max-md:gap-0">
            <div class="flex flex-col items-stretch w-[37%] max-md:w-full max-md:ml-0">
              <div class="justify-center items-center flex flex-col max-md:mt-10">
                <div
                  class="stroke-[1.866px] self-stretch flex gap-0.5 pr-5 py-2.5 rounded-[50%] items-start max-md:justify-center">
                  <div class="stroke-[1.866px] flex w-3 shrink-0 h-[13px] flex-col mt-14 rounded-[50%] max-md:mt-10">
                  </div>
                  <div
                    class="self-stretch flex grow basis-[0%] flex-col justify-center items-stretch pl-5 pr-2 py-4 rounded-[50%]">
                    <div class="flex flex-col items-stretch px-8 py-8 rounded-[50%] max-md:px-5">
                      <div class="text-zinc-800 text-center text-3xl font-bold whitespace-nowrap">
                        01
                      </div>
                      <div class="text-zinc-800 text-center text-xs font-medium uppercase whitespace-nowrap mt-1.5">
                        Step
                      </div>
                    </div>
                  </div>
                  <div class="stroke-[1.866px] self-center flex w-3 shrink-0 h-[13px] flex-col my-auto rounded-[50%]">
                  </div>
                </div>
                <div class="text-neutral-700 text-center text-xl font-bold whitespace-nowrap mt-5">
                  Explore Our Tree Collection:
                </div>
                <div class="text-neutral-400 text-center text-xs font-medium leading-4 self-stretch mt-4">
                  Browse through our diverse selection of trees. Each tree comes with its unique characteristics,
                  benefits, and story. Find the one that resonates with you.
                </div>
              </div>
            </div>
            <div class="flex flex-col items-stretch w-[37%] ml-5 max-md:w-full max-md:ml-0">
              <div class="justify-end items-stretch flex flex-col max-md:mt-10">
                <div class="stroke-[1.866px] flex gap-0.5 pr-5 py-2.5 rounded-[50%] items-start max-md:justify-center">
                  <div class="stroke-[1.866px] flex w-3 shrink-0 h-[13px] flex-col mt-14 rounded-[50%] max-md:mt-10">
                  </div>
                  <div
                    class="self-stretch flex grow basis-[0%] flex-col justify-center items-stretch pl-5 pr-2 py-4 rounded-[50%]">
                    <div class="flex flex-col items-stretch pl-8 pr-7 py-8 rounded-[50%] max-md:px-5">
                      <div class="text-zinc-800 text-center text-3xl font-bold whitespace-nowrap">
                        02
                      </div>
                      <div class="text-zinc-800 text-center text-xs font-medium uppercase whitespace-nowrap mt-1.5">
                        Step
                      </div>
                    </div>
                  </div>
                  <div class="stroke-[1.866px] self-center flex w-3 shrink-0 h-[13px] flex-col my-auto rounded-[50%]">
                  </div>
                </div>
                <div class="text-neutral-700 text-center text-xl font-bold whitespace-nowrap mt-5">
                  Select and Personalize:
                </div>
                <div class="text-neutral-400 text-center text-xs font-medium leading-4 mt-4">
                  Choose the tree you'd like to adopt and personalize the adoption details. Add a custom name for your
                  tree and select any additional features or services to enhance your adoption experience.
                </div>
              </div>
            </div>
            <div class="flex flex-col items-stretch w-[27%] ml-5 max-md:w-full max-md:ml-0">
              <div class="justify-end items-stretch flex grow flex-col max-md:mt-10">
                <div class="stroke-[1.866px] flex gap-0.5 pr-5 py-2.5 rounded-[50%] items-start max-md:justify-center">
                  <div class="stroke-[1.866px] flex w-3 shrink-0 h-[13px] flex-col mt-14 rounded-[50%] max-md:mt-10">
                  </div>
                  <div
                    class="self-stretch flex grow basis-[0%] flex-col justify-center items-stretch pl-5 pr-2 py-4 rounded-[50%]">
                    <div class="flex flex-col items-stretch px-8 py-8 rounded-[50%] max-md:px-5">
                      <div class="text-zinc-800 text-center text-3xl font-bold whitespace-nowrap">
                        03
                      </div>
                      <div class="text-zinc-800 text-center text-xs font-medium uppercase whitespace-nowrap mt-1.5">
                        Step
                      </div>
                    </div>
                  </div>
                  <div class="stroke-[1.866px] self-center flex w-3 shrink-0 h-[13px] flex-col my-auto rounded-[50%]">
                  </div>
                </div>
                <div class="text-neutral-700 text-center text-xl font-bold whitespace-nowrap mt-5">
                  Become a Growth Partner:
                </div>
                <div class="text-neutral-400 text-center text-xs font-medium leading-4 mt-4">
                  Complete the adoption by making a contribution. As a Growth Partner, you'll receive regular updates on
                  your tree's progress, including growth milestones and the share of produce you'll be receiving as a part
                  of our unique Adopt a Tree initiative.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <br>
  <br>
  <div class="justify-center items-stretch bg-gray-700 flex flex-col py-2 rounded-[70px]">
    <div
      class="items-center bg-purple-50 flex flex-col pt-8 pb-3 px-16 rounded-[60px] max-md:max-w-[800px] max-md:mr-0.5 max-md:px-5">
      <div class="flex flex-col items-center px-5">
        <div
          class="justify-center text-zinc-800 text-center text-4xl font-bold leading-[65px] max-w-[833px] max-md:max-w-full">
          "Cultivating a Forest of Change: Empowering Everyone to Adopt Trees and Create a Greener Tomorrow."
        </div>
        <div class="self-stretch w-full mt-2 max-md:max-w-full">
          <div class="gap-5 flex max-md:flex-col max-md:items-stretch max-md:gap-0">
            <div class="flex flex-col items-stretch w-6/12 max-md:w-full max-md:ml-0">
              <div class="items-stretch flex grow flex-col pt-2 pb-12 max-md:max-w-full max-md:mt-10">
                <div class="flex justify-between gap-5 items-start max-md:max-w-full max-md:flex-wrap">
                  <img
                    src="https://cdn.builder.io/api/v1/image/assets/TEMP/ebf6ada1ce4b822039fc1ddabcb048a4c91f51078f2c18954492e2265e1835b6?apiKey=5b2da896aa694c5eb6df24abe3dcfabc&"
                    class="aspect-square object-contain object-center w-14 shadow-lg overflow-hidden shrink-0 max-w-full" />
                  <div class="items-stretch flex grow basis-[0%] flex-col pr-2.5 py-px">
                    <div class="text-gray-800 text-base font-bold leading-6">
                      Nature Enthusiast

                    </div>
                    <div class="text-gray-800 text-sm leading-6 mt-2">
                      Embark on a fulfilling journey to support environmental sustainability through our tree adoption
                      platform. We ensure the authenticity of each adopted tree, providing a seamless and affordable
                      process. Bid farewell to environmental concerns and reclaim your role in nurturing our planet.
                      User-friendly and reliable, it's your gateway to making a positive impact on the Earth.
                    </div>
                  </div>
                </div>
                <div class="flex justify-between gap-5 mt-5 items-start max-md:max-w-full max-md:flex-wrap">
                  <img
                    src="https://cdn.builder.io/api/v1/image/assets/TEMP/5a4c4e5d0d16428e5c8283634f794a2afa5f8650efd407d35d42d876c7759a81?apiKey=5b2da896aa694c5eb6df24abe3dcfabc&"
                    class="aspect-square object-contain object-center w-14 shadow-lg overflow-hidden shrink-0 max-w-full" />
                  <div class="items-stretch flex grow basis-[0%] flex-col pr-5">
                    <div class="text-gray-800 text-base font-bold leading-6">
                      Green Guardians
                    </div>
                    <div class="text-gray-800 text-sm leading-6 mt-2.5">
                      Join our platform to boost your commitment to tree conservation and increase your impact. We offer a
                      seamless, low-cost solution for authentic tree adoptions, simplifying the process and empowering you
                      to stand out as a trusted advocate for green initiatives.and
                      stand out as a trusted broker committed to transparency.
                    </div>
                  </div>
                </div>
                <div
                  class="flex justify-between gap-5 mt-11 mb-12 items-start max-md:max-w-full max-md:flex-wrap max-md:my-10">
                  <img
                    src="https://cdn.builder.io/api/v1/image/assets/TEMP/c249f87753c53a019f009e22b00187d0554fb584cc36ecb16f1aa489eb6bb538?apiKey=5b2da896aa694c5eb6df24abe3dcfabc&"
                    class="aspect-square object-contain object-center w-14 fill-white overflow-hidden shrink-0 max-w-full" />
                  <div class="items-stretch flex grow basis-[0%] flex-col py-px">
                    <div class="text-gray-800 text-base font-bold leading-6">
                      Earth Champions
                    </div>
                    <div class="text-gray-800 text-sm leading-6 mt-2">
                      Become an Earth Champion! Our platform guarantees the inclusion of only genuine tree adoptions in
                      your mission to create a healthier planet. This cost-effective and efficient solution streamlines
                      the adoption validation process, allowing you to lead in environmental stewardship while upholding a
                      reputation for trust and sustainability.
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="flex flex-col items-stretch w-6/12 ml-5 max-md:w-full max-md:ml-0 ">
              <img src="@/components/icons/savetree-banner.jpeg"
                class="aspect-[0.97] object-contain object-center w-full overflow-hidden max-md:max-w-full max-md:mt-10" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <br>
  <br>
  <br>
  <!-- our mission / our vission -->
  <div class="flex flex-col px-5 mb-8 mx-10">
    <div class="text-black text-center text-4xl font-semibold leading-[55px] self-center max-w-[487px]">
      Our Mission / Vision
    </div>
    <img
      src="https://cdn.builder.io/api/v1/image/assets/TEMP/fc14f0a61183607c8c4d311c4561e10addde3f59989252392f5c601b31086486?"
      class="aspect-[100] object-contain object-center w-[400px] fill-[linear-gradient(90deg,#7C14FD_1.09%,rgba(124,20,253,0.29)_99.99%)] overflow-hidden self-center max-w-full mt-6" />

    <div class="z-[1] flex w-[772px] max-w-full flex-col items-stretch ml-3.5 mt-4 self-start">
      <div
        class="text-[#efe8f8] font-bold text-9xl leading-[55px] z-[1] max-md:max-w-full max-md:text-4xl max-md:leading-5">
        01
      </div>
      <div class="-mt-6 max-md:max-w-full bg-card">
        <div class="gap-5 flex max-md:flex-col max-md:items-stretch max-md:gap-0">
          <div class="flex flex-col items-stretch w-[39%] max-md:w-full max-md:ml-0">
            <img src="@/components/icons/cooltree.png"
              class="aspect-[1.31] object-contain object-center w-full justify-center items-center overflow-hidden grow max-md:mt-10" />
          </div>
          <div class="flex flex-col items-stretch w-[61%] ml-5 max-md:w-full max-md:ml-0">
            <div class="flex flex-col mt-10 pr-7 items-start max-md:max-w-full max-md:pr-5">
              <div class="text-violet-600 text-3xl font-bold leading-10 self-stretch">
                "Sowing Seeds of Change for a Sustainable Tomorrow"
              </div>
              <div class="flex w-[75px] shrink-0 h-0.5 flex-col mt-5 rounded-[839.844px]"></div>
              <div class="text-black text-base font-semibold leading-7 self-stretch max-w-[429px] mt-5">
                We are on a mission to cultivate a greener future by promoting widespread tree adoption. Through our
                platform, we aim to empower individuals and organizations to contribute actively to environmental
                conservation, fostering a sense of responsibility and connection with nature.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- 2 -->
    <div class="z-[1] flex w-[772px] max-w-full flex-col items-stretch ml-3.5 mt-4 self-end">
      <div
        class="text-[#efe8f8] font-bold text-9xl leading-[55px] z-[1] max-md:max-w-full max-md:text-4xl max-md:leading-5 self-end">
        02
      </div>
      <div class="-mt-6 max-md:max-w-full bg-card">
        <div class="gap-5 flex max-md:flex-col max-md:items-stretch max-md:gap-0">
          <div class="flex flex-col items-stretch w-[39%] max-md:w-full max-md:ml-0">
            <img src="@/components/icons/oldtree.svg" alt="finance alt text"
              class="aspect-[1.31] object-contain object-center w-full justify-center items-center overflow-hidden grow max-md:mt-10" />
          </div>
          <div class="flex flex-col items-stretch w-[61%] ml-5 max-md:w-full max-md:ml-0">
            <div class="flex flex-col mt-10 pr-7 items-start max-md:max-w-full max-md:pr-5">
              <div class="text-violet-600 text-3xl font-bold leading-10 self-stretch">
                "Harmony in Every Leaf: Nurturing a Global Ecosystem"
              </div>
              <div class="flex w-[75px] shrink-0 h-0.5 flex-col mt-5 rounded-[839.844px]"></div>
              <div class="text-black text-base font-semibold leading-7 self-stretch max-w-[429px] mt-5">
                Our mission is to create harmony in every corner of the world through tree adoption. By facilitating the
                growth of diverse ecosystems, we strive to enhance the well-being of our planet and inspire a collective
                commitment to ecological balance.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- 02 end -->

    <!-- 03 -->

    <div class="z-[1] flex w-[772px] max-w-full flex-col items-stretch ml-3.5 mt-4 ">
      <div
        class="text-[#efe8f8] font-bold text-9xl leading-[55px] z-[1] max-md:max-w-full max-md:text-4xl max-md:leading-5 ">
        03
      </div>
      <div class="-mt-6 max-md:max-w-full bg-card">
        <div class="gap-5 flex max-md:flex-col max-md:items-stretch max-md:gap-0">
          <div class="flex flex-col items-stretch w-[39%] max-md:w-full max-md:ml-0">
            <img src="@/components/icons/carold.svg" alt="finance alt text"
              class="aspect-[1.31] object-contain object-center w-full justify-center items-center overflow-hidden grow max-md:mt-10" />
          </div>
          <div class="flex flex-col items-stretch w-[61%] ml-5 max-md:w-full max-md:ml-0">
            <div class="flex flex-col mt-10 pr-7 items-start max-md:max-w-full max-md:pr-5">
              <div class="text-violet-600 text-3xl font-bold leading-10 self-stretch">
                "A World Where Every Tree Counts"
              </div>
              <div class="flex w-[75px] shrink-0 h-0.5 flex-col mt-5 rounded-[839.844px]"></div>
              <div class="text-black text-base font-semibold leading-7 self-stretch max-w-[429px] mt-5">
                Our vision is to create a world where every tree is valued and contributes to a flourishing ecosystem. We
                envision a global community actively engaged in nurturing and preserving the environment, ensuring a
                sustainable and vibrant future for generations to come.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- 03 end -->

    <!-- 04 -->

    <div class="z-[1] flex w-[772px] max-w-full flex-col items-stretch ml-3.5 mt-4 self-end">
      <div
        class="text-[#efe8f8] font-bold text-9xl leading-[55px] z-[1] max-md:max-w-full max-md:text-4xl max-md:leading-5 self-end">
        04
      </div>
      <div class="-mt-6 max-md:max-w-full bg-card">
        <div class="gap-5 flex max-md:flex-col max-md:items-stretch max-md:gap-0">
          <div class="flex flex-col items-stretch w-[39%] max-md:w-full max-md:ml-0">
            <img src="@/components/icons/utree.png" alt="save tree"
              class="aspect-[1.31] object-contain object-center w-full justify-center items-center overflow-hidden grow max-md:mt-10" />
          </div>
          <div class="flex flex-col items-stretch w-[61%] ml-5 max-md:w-full max-md:ml-0">
            <div class="flex flex-col mt-10 pr-7 items-start max-md:max-w-full max-md:pr-5">
              <div class="text-violet-600 text-3xl font-bold leading-10 self-stretch">
                "Empowering Communities, Enriching Biodiversity"
              </div>
              <div class="flex w-[75px] shrink-0 h-0.5 flex-col mt-5 rounded-[839.844px]"></div>
              <div class="text-black text-base font-semibold leading-7 self-stretch max-w-[429px] mt-5">
                We aspire to see communities empowered through tree adoption, enriching biodiversity and creating
                resilient ecosystems. Our vision is to be a catalyst for positive change, connecting people with nature
                and fostering a deep appreciation for the interconnectedness of all living things.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- 04 end -->
  </div>



  <br>
  <br>


  <div class="flex justify-center items-stretch max-w-full bg-purple-50 flex-col pl-4 mx rounded-[70px]">
    <div class="max-md:max-w-full flex-grow min-h-[0]">
      <div class="gap-10 flex max-md:flex-col max-md:items-stretch max-md:gap-0">

        <div class="flex flex-col items-stretch w-[50%] max-md:w-full max-md:ml-0">
          <img src="@/components/icons/faq.jpeg" alt="faq"
            class="aspect-[2] object-contain object-center w-auto items-start overflow-hidden max-md:max-w-full max-md:mt-2" />
        </div>
        <div class="flex flex-col items-stretch w-[46%] max-md:w-full max-md:ml-0">
          <div class="items-stretch flex grow flex-col pb-6 max-md:max-w-full max-md:mt-10">
            <div class="text-black text-3xl font-bold leading-10 max-md:max-w-full">
              <br>
              <br>
              Frequently Asked Questions
            </div>
            <div class="items-start bg-slate-200 flex shrink-0 h-0.5 flex-col mt-5 mr-10 max-md:max-w-full"></div>
            <div class="flex flex-col mt-6 items-start max-md:max-w-full max-md:flex-wrap">
              <div class="faq-question" v-for="faq in faqs" :key="faq.id">
                <div class="flex justify-between items-center">
                  <div @click="toggleAnswer(faq.id)"
                    class="text-black text-lg font-bold leading-6 grow whitespace-nowrap max-md:max-w-full cursor-pointer">
                    {{ faq.question }}
                  </div>
                  <button @click="toggleAnswer(faq.id)" class="text-3xl font-bold focus:outline-none mr-6  end-0">
                    {{ showAnswer[faq.id] ? '-' : '+' }}
                  </button>
                </div>
                <div v-show="showAnswer[faq.id]"
                  class="text-zinc-700 text-opacity-80 text-base leading-6 mt-4 max-md:max-w-full pr-10">
                  {{ faq.answer }}
                </div>
                <div class="items-start bg-slate-200 flex shrink-0 h-0.5 flex-col mt-5 mr-10 max-md:max-w-full"></div>
              </div>
              <br>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <br>
  <br>
</template>
  
<script>
import backgroundImage from '@/components/icons/hero-bg.png';
export default {
  data() {
    return {
      backgroundImage,
      showAnswer: {},
      faqs: [
        { id: 1, question: 'How does the tree adoption process work?', answer: 'Select a tree, personalize your adoption details, and contribute to become a Growth Partner. Receive updates on your tree\ns progress and share in the produce.' },
        { id: 2, question: 'Can I visit the adopted tree?', answer: 'While physical visits might not be possible, our interactive dashboard allows you to monitor your tree\ns growth and receive regular updates on its well- being.' },
        // { id: 3, question: 'Where can I watch?', answer: 'Nibh quisque suscipit fermentum netus nulla cras porttitor euismod nulla. Orci, dictumst nec aliquet id ullamcorper venenatis.' },
        // { id: 4, question: 'Dummy question2?', answer: 'Dummy sjakf fdsajkfd ajfkdlsa jfd sakfda fjdksla;f jfkdlsa jfdsklaj fjdksal fjdsksal fjdksa fjdksal jfdkas jf answer mmy sjakf fdsajkfd ajfkdlsa jfd sakfda fjdksla;f jfkdlsa jfdsklaj fjdksal fjdsksal fjdksa fjdksal jfdka3.' },
        // { id: 5, question: 'Where can I watch?', answer: 'Nibh quisque suscipit fermentum netus nulla cras porttitor euismod nulla. Orci, dictumst nec aliquet id ullamcorper venenatis.' },
        // { id: 6, question: 'Dummy question2?', answer: 'Dummy sjakf fdsajkfd ajfkdlsa jfd sakfda fjdksla;f jfkdlsa jfdsklaj fjdksal fjdsksal fjdksa fjdksal jfdkas jf answer mmy sjakf fdsajkfd ajfkdlsa jfd sakfda fjdksla;f jfkdlsa jfdsklaj fjdksal fjdsksal fjdksa fjdksal jfdka3.' },
        // { id: 7, question: 'Where can I watch?', answer: 'Nibh quisque suscipit fermentum netus nulla cras porttitor euismod nulla. Orci, dictumst nec aliquet id ullamcorper venenatis.' },
        { id: 8, question: 'environmental impact of tree adoption?', answer: 'Tree adoption contributes to carbon offset, biodiversity preservation, and community development. It\ns a sustainable way to make a positive impact on the planet.' },
        // Add more FAQs as needed
      ],
    };
  },
  methods: {
    toggleAnswer(id) {
      this.showAnswer[id] = !this.showAnswer[id];
    },
  },
};
</script>

<style scoped>
.bg-card {
  width: 100%;
  height: 100%;
  background: white;
  box-shadow: 0px 57.94921875px 95.7421875px rgba(124, 20, 253, 0.08);
  border-radius: 8.40px
}

.gradient-txt {
  color: transparent !important;

  background-image: linear-gradient(to right, #9A4EB7, #536DFE, #29B8FF);
  background-clip: text;
  -webkit-background-clip: text;

  text-align: center;
  font-size: 1.25rem;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

@media not all and (max-width: 768px) {
  .faq-bx {
    margin-bottom: -200px;
    overflow: hidden;
  }
}
</style>