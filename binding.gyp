{
  'includes': [ 'common.gypi' ],
  'variables': {
      'std%':'ansi',
      'runtime_link%':'shared',
      'NODEMAPNIK_DIR%':'.'
  },
  'conditions': [
      ['OS=="win"', {
        'variables': {
          'NODEMAPNIK_DIR%':'C:/dev2/node-mapnik'
        }
      }]
  ],
  'targets': [
    {
      'target_name': 'action_before_build',
      'hard_dependency': 1,
      'type': 'none',
      'actions': [
          {
            'action_name': 'generate_setting',
            'inputs': [
              'gen_settings.py'
            ],
            'outputs': [
              '<(SHARED_INTERMEDIATE_DIR)/mapnik_settings.js'
            ],
            'action': ['python', 'gen_settings.py', '<(SHARED_INTERMEDIATE_DIR)/mapnik_settings.js']
          }
      ],
      'copies': [
          {
            'files': [ '<(SHARED_INTERMEDIATE_DIR)/mapnik_settings.js' ],
            'destination': '<(module_path)'
          }
      ]
    },
    {
      'target_name': '<(module_name)',
      'dependencies': [ 'action_before_build' ],
      'sources': [
          "src/node_mapnik.cpp",
          "src/mapnik_map.cpp",
          "src/mapnik_color.cpp",
          "src/mapnik_geometry.cpp",
          "src/mapnik_feature.cpp",
          "src/mapnik_image.cpp",
          "src/mapnik_image_view.cpp",
          "src/mapnik_grid.cpp",
          "src/mapnik_grid_view.cpp",
          "src/mapnik_memory_datasource.cpp",
          "src/mapnik_palette.cpp",
          "src/mapnik_projection.cpp",
          "src/mapnik_layer.cpp",
          "src/mapnik_datasource.cpp",
          "src/mapnik_featureset.cpp",
          "src/mapnik_expression.cpp",
          "src/mapnik_cairo_surface.cpp",
      ],
      'include_dirs': [
          '<(SHARED_INTERMEDIATE_DIR)/',
          './src'
      ],
      'conditions': [
        ['OS=="win"', {
            'include_dirs':[
                '<!@(mapnik-config --includes)',
                '<!@(mapnik-config --dep-includes)',
              ],
            'defines': ['NOMINMAX','<!@(mapnik-config --defines)'],
            'libraries': [
                '<!@(mapnik-config --libs)',
                '<!@(mapnik-config --dep-libs)',
            ],
            'msvs_disabled_warnings': [ 4244,4005,4506,4345,4804 ],
            'msvs_settings': {
              'VCCLCompilerTool': {
                # uneeded now that they are in common.gypi VCCLCompilerTool
                #'AdditionalOptions': [
                #  '/GR',
                #  '/MD',
                #  '/EHsc'
                #]
              },
              'VCLinkerTool': {
                'AdditionalOptions': [
                    # https://github.com/mapnik/node-mapnik/issues/74
                    '/FORCE:MULTIPLE'
                ],
                'AdditionalLibraryDirectories': [
                    '<!@(mapnik-config --ldflags)',
                ],
              },
            }
        },{
            'cflags_cc!': ['-fno-rtti', '-fno-exceptions'],
            'cflags_cc' : [
                '<!@(mapnik-config --cflags)',
            ],
            'libraries':[
                '<!@(mapnik-config --libs)',
                '<!@(mapnik-config --ldflags)',
            ],
            'conditions': [
              ['runtime_link == "static"', {
                  'libraries': [
                    '<!@(mapnik-config --dep-libs)'
                   ]
              }]
            ],
            'xcode_settings': {
              'OTHER_CPLUSPLUSFLAGS':[
                  '<!@(mapnik-config --cflags)',
              ],
              'OTHER_CFLAGS':[
                  '<!@(mapnik-config --cflags)',
              ],
              'GCC_ENABLE_CPP_RTTI': 'YES',
              'GCC_ENABLE_CPP_EXCEPTIONS': 'YES'
            }
        },
        ],
        ['std == "c++11"', {
            'cflags_cc' : [
                '-std=c++11',
            ],
            'xcode_settings': {
              'OTHER_CPLUSPLUSFLAGS':['-std=c++11','-stdlib=libc++'],
              'OTHER_LDFLAGS':['-stdlib=libc++'],
              'CLANG_CXX_LANGUAGE_STANDARD':'c++11'
            }
        }]
      ]
    },
    {
      'target_name': 'action_after_build',
      'type': 'none',
      'dependencies': [ '<(module_name)' ],
      'copies': [
          {
            'files': [ '<(PRODUCT_DIR)/<(module_name).node' ],
            'destination': '<(module_path)'
          }
      ]
    }
  ]
}
