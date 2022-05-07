var fs = require('fs');
var dict = {"one" : [15, 4.5],
    "two" : [34, 3.3],
    "three" : [67, 5.0],
    "four" : [32, 4.1]};

function main(){
    let len = 2822 + 166
    for (let index = 2998; index <= 3000; index++) {        
        const myJson =  {
            "name": `The bauss girls #${index}`,
            "symbol": "BG",
            "description": "The Official Bauss girls 3000 collection..",
            "seller_fee_basis_points": 1000,
            "image": `${index}.png`,
            "attributes": [
                {
                    "trait_type": "accessories",
                    "value": "3-01"
                },
                {
                    "trait_type": "Backgrounds",
                    "value": "11"
                },
                {
                    "trait_type": "body",
                    "value": "african-01"
                },
                {
                    "trait_type": "eye brows",
                    "value": "3-01"
                },
                {
                    "trait_type": "eyes",
                    "value": "3-01"
                },
                {
                    "trait_type": "hairs",
                    "value": "6-01"
                },
                // {
                //     "trait_type": "Hat",
                //     "value": "1-01"
                // },
                {
                    "trait_type": "lips",
                    "value": "3-01"
                },
                // {
                //     "trait_type": "tattoo",
                //     "value": "1-01"
                // }
            ],
            "properties": {
                "creators": [{"address": "Cked4ixGwxvjopepTmSiUyYpxDZZoaomHEgi7hnJ3bJa", "share": 100}],
                "files": [{"uri": `${index}.png`, "type": "image/png"}]
            },
            "collection": {"name": "Pilot", "family": "White And Asians"}
        }
        const dictstring = JSON.stringify(myJson);
        // fs.rename(`images/White And Asian/Degree Holder/images/${index}.png`, `images/White And Asian/Degree Holder/${index+2823}.png`, function(err, result) {
        //     if(err) console.log('error', err);
        // });
        fs.writeFile(`candy-metadata/Extra/${index}.json`, dictstring, function(err, result) {
            if(err) console.log('error', err);
        });
    }
}

main()