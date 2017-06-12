from politeauthority.meta import Meta
m = Meta()
m.schema = 'stocks'
meta_info = {}
meta_info['entity_id'] = 10
meta_info['entity_type'] = 'test'
meta_info['key'] = 'demo'
meta_info['value'] = {'test': 12}
meta_info['type'] = 'pickle'

m.save(meta_info)
