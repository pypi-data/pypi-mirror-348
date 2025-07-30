
let fill_demo = document.getElementById("fill_demo")
if (fill_demo) {
    fill_demo.addEventListener('click', function () {
        document.getElementsByName("sequence")[0].value = "GCTTGCATGCCTGCAGGTCGACTCTAGAGGATCCCCCTACATTTTAGCATCAGTGAGTACAGCATGCTTACTGGAAGAGAGGGTCATGCAACAGATTAGGAGGTAAGTTTGCAAAGGCAGGCTAAGGAGGAGACGCACTGAATGCCATGGTAAGAACTCTGGACATAAAAATATTGGAAGTTGTTGAGCAAGTNAAAAAAATGTTTGGAAGTGTTACTTTAGCAATGGCAAGAATGATAGTATGGAATAGATTGGCAGAATGAAGGCAAAATGATTAGACATATTGCATTAAGGTAAAAAATGATAACTGAAGAATTATGTGCCACACTTATTAATAAGAAAGAATATGTGAACCTTGCAGATGTTTCCCTCTAGTAG"
        document.getElementsByName("seq_start")[0].value = 36
        document.getElementsByName("seq_end")[0].value = 342
    })
}

let clear = document.getElementById("clear")
if (clear) {
    clear.onclick = function () {
        document.getElementsByName("sequence")[0].value = ""
        document.getElementsByName("seq_start")[0].value = null
        document.getElementsByName("seq_end")[0].value = null
        window.location.href = "/primer"
    }
}
