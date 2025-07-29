schemarule = {
  "type": "object", 
  "properties": {

    "browser": {
      "type": "object",
      "properties": {
        "mode": {
          "type": "string", 
          "enum":["standard","headless","debug","login","proxy","remote"] 
        }, 
        "path": {
          "type": "string", 
          "enum":["config","env","manager"] 
        },
      },
      "required": ["mode","path"]
    },

    "basic": {
      "type": "object",
      "properties": {
        "site":{
          "type": "string",
          "not": { "pattern": "^$" },
        },
        "lang":{
          "type": "string",
          "enum":["cn","en"] 
        },
        "brief_url": {
          "type": "string",
          "format": "url",
          "not": { "pattern": "^$" },
        }, 
      },
      "required": ["site","lang","brief_url"]
    },
    
    "brief_preparation":{
      "type": ["object","null"],
    },

    "brief_execution":{
      "type": ["object","null"],
    },

    "brief_cleanup":{
      "type": ["object","null"],
    },

    "material_preparation":{
      "type": ["object","null"],
    },

    "material_execution":{
      "type": ["object","null"],
    },

    "material_cleanup":{
      "type": ["object","null"],
    },
  },

  "required": ["browser","basic","brief_preparation","brief_execution","brief_cleanup","material_preparation","material_execution","material_cleanup"],
}