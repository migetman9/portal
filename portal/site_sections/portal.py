from portal import *

@all_renderable(c.PORTAL)
class Root:
    @site_mappable
    @unrestricted
    def index(self, category=None, key=None, these=None, are=None, protective=None, filler=None, session=None, message=''):
        items = session.query(PortalItem).all()
        if category:
            category_item = session.query(PortalCategory).filter(PortalCategory.key == category).first()
            if category_item:
                if key:
                    item = session.query(PortalItem).filter(PortalItem.key == key and PortalItem.category_id == category_item.id).first()
                    if item:
                        raise HTTPRedirect(item.link)
                    else:
                        message = 'Item Not Found {} {}'.format(key, category)
                else:
                    items = category_item.items
        return {
            'message': message,
            'items': items
        }

    @unrestricted
    def default(self, category=None, key=None, these=None, are=None, protective=None, filler=None, session=None, **params):
        if category:
            category_item = session.query(PortalCategory).filter(PortalCategory.key == category).first()
            if category_item:
                if key:
                    item = session.query(PortalItem).filter(PortalItem.key == key and PortalItem.category_id == category_item.id).first()
                    if item:
                        raise HTTPRedirect(item.link)
                else:
                    raise HTTPRedirect("index/{}".format(category_item.key))
        raise HTTPRedirect("index")

    @site_mappable
    def add_category(self, session, message='', new_entry=None, **params):
        category_item = session.portal_category(params)
        if 'name' in params:
            session.add(category_item)
            session.commit()
        return {
            'message': message,
            'item': category_item,
            'categories': session.query(PortalCategory).all(),
            'new_entry': new_entry
        }

    @site_mappable
    def add_item(self, session, message='', new_entry=None, **params):
        portal_item = session.portal_item(params)
        if 'name' in params:
            session.add(portal_item)
            session.commit()
        return {
            'message': message,
            'item': portal_item,
            'items': session.query(PortalItem).all(),
            'categories': session.query(PortalCategory).all(),
            'new_entry': new_entry
        }

    def delete(self, session, message='', option='', **params):
        choices = {
            'item': PortalItem,
            'category': PortalCategory
        }
        message = 'ID not in parameters'
        if 'id' in params:
            choice = choices.get(option)
            message = "Option '{}' not found".format(option)
            if choice:
                item = session.query(choice).filter(choice.id == params['id']).first()
                message = '{} has been deleted'.format(item.name)
                session.delete(item)
                session.commit()

        raise HTTPRedirect('add_{}?message={}'.format(option, message))

